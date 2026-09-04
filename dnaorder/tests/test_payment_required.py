"""SubmissionType.payment_required and the per-submission snapshot of it.

Payment is only displayed and validated when required.  The requirement is
copied onto the submission when it is created (``Submission.payment_required``),
so a submission keeps the arrangement it was submitted with, payment plugin or
none at all, even if its type changes later.  Moving a submission to a
different type is the one case where the new type's requirement applies.

The fixture labs have no payment plugin configured, so the default UC Davis
payment serializer applies whenever payment is required.
"""
from dnaorder.models import Submission
from dnaorder.tests.base import ApiTestCase, make_submission, make_submission_type
from plugins import PluginManager

#: Minimal valid payment for the default (UCD) payment serializer.
CREDIT_CARD = {"payment_type": "Credit Card", "payment_info": ""}


def submission_payload(submission_type, **overrides):
    """A complete, valid POST/PUT body for the writable submission serializer."""
    payload = {
        "type": submission_type.id,
        "first_name": "Sub",
        "last_name": "Mitter",
        "email": "submitter@example.com",
        "phone": "555-0100",
        "pi_first_name": "Prof",
        "pi_last_name": "Essor",
        "pi_email": "pi@example.com",
        "pi_phone": "555-0101",
        "institute": "Dept of Testing",
        "contacts": [],
        "submission_data": {},
    }
    payload.update(overrides)
    return payload


class PaymentRequiredFixture(ApiTestCase):
    """The standard fixture plus a Lab A type that does not require payment."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.type_free = make_submission_type(
            cls.lab_a, name="Lab A Free Type", payment_required=False
        )

    @staticmethod
    def url(submission):
        return "/api/submissions/{}/".format(submission.id)


class SubmissionTypePaymentRequiredTests(PaymentRequiredFixture):
    def test_defaults_to_required(self):
        self.assertTrue(self.type_a.payment_required)
        self.assertTrue(self.sub_a.payment_required)

    def test_flag_is_exposed_wherever_types_are_served(self):
        detail = self.as_anon().get("/api/submission_types/{}/".format(self.type_free.id))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["payment_required"], False)

        lab = self.as_anon().get("/api/labs/lab-a/")
        self.assertEqual(lab.status_code, 200, lab.content)
        flags = {t["id"]: t["payment_required"] for t in lab.data["submission_types"]}
        self.assertIs(flags[self.type_a.id], True)
        self.assertIs(flags[self.type_free.id], False)

        sub = make_submission(self.type_free)
        detail = self.as_user(self.lab_a_member).get(self.url(sub))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["type"]["payment_required"], False)

    def test_lab_member_can_toggle_flag(self):
        resp = self.as_user(self.lab_a_member).patch(
            "/api/submission_types/{}/".format(self.type_a.id),
            {"payment_required": False}, format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.type_a.refresh_from_db()
        self.assertFalse(self.type_a.payment_required)

    def test_toggling_type_leaves_existing_submissions_alone(self):
        self.type_a.payment_required = False
        self.type_a.save()
        self.sub_a.refresh_from_db()
        self.assertTrue(self.sub_a.payment_required)


class SnapshotModelTests(PaymentRequiredFixture):
    def test_snapshot_is_taken_from_the_type_on_create(self):
        self.assertFalse(make_submission(self.type_free).payment_required)
        self.assertTrue(make_submission(self.type_a).payment_required)

    def test_snapshot_is_not_retaken_on_later_saves(self):
        sub = make_submission(self.type_free)
        self.type_free.payment_required = True
        self.type_free.save()
        sub.save()
        sub.refresh_from_db()
        self.assertFalse(sub.payment_required)


class CreateSubmissionPaymentTests(PaymentRequiredFixture):
    def test_payment_is_required_by_default(self):
        resp = self.as_anon().post("/api/submissions/", submission_payload(self.type_a), format="json")
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)

    def test_payment_is_validated_and_stored_when_required(self):
        payload = submission_payload(self.type_a, payment=CREDIT_CARD)
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        sub = Submission.objects.get(pk=resp.data["id"])
        self.assertTrue(sub.payment_required)
        self.assertEqual(sub.payment["payment_type"], "Credit Card")

    def test_no_payment_needed_when_type_does_not_require_it(self):
        resp = self.as_anon().post("/api/submissions/", submission_payload(self.type_free), format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        sub = Submission.objects.get(pk=resp.data["id"])
        self.assertFalse(sub.payment_required)
        self.assertEqual(sub.payment, {})
        self.assertIs(resp.data["payment_required"], False)
        self.assertEqual(resp.data["payment"], {})

    def test_payment_sent_for_no_payment_type_is_discarded_unvalidated(self):
        # e.g. a stale browser draft.  This UCD payment would be rejected if validated.
        payload = submission_payload(
            self.type_free, payment={"payment_type": "DaFIS", "payment_info": "not-an-account"}
        )
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(Submission.objects.get(pk=resp.data["id"]).payment, {})

    def test_snapshot_cannot_be_set_by_the_client(self):
        payload = submission_payload(self.type_a, payment=CREDIT_CARD, payment_required=False)
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertTrue(Submission.objects.get(pk=resp.data["id"]).payment_required)

        payload = submission_payload(self.type_free, payment_required=True)
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertFalse(Submission.objects.get(pk=resp.data["id"]).payment_required)


class ReadSubmissionPaymentTests(PaymentRequiredFixture):
    def test_no_payment_submission_returns_empty_payment(self):
        sub = make_submission(self.type_free)
        detail = self.as_user(self.lab_a_member).get(self.url(sub))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["payment_required"], False)
        self.assertEqual(detail.data["payment"], {})
        # List views share one serializer across rows; they must not dress the
        # empty payment up with blank display fields either.
        listing = self.as_user(self.lab_a_member).get(
            "/api/submissions/?lab=lab-a&id={}".format(sub.id)
        )
        self.assertEqual(listing.status_code, 200, listing.content)
        self.assertEqual(listing.data["results"][0]["payment"], {})

    def test_paid_submission_still_returns_display(self):
        sub = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        detail = self.as_user(self.lab_a_member).get(self.url(sub))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["payment_required"], True)
        self.assertEqual(detail.data["payment"]["display"]["Payment Type"], "Credit Card")


class UpdateSubmissionPaymentTests(PaymentRequiredFixture):
    def test_no_payment_submission_stays_that_way_when_type_starts_requiring_payment(self):
        sub = make_submission(self.type_free)
        self.type_free.payment_required = True
        self.type_free.save()
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_free), format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertFalse(sub.payment_required)
        self.assertEqual(sub.payment, {})

    def test_paid_submission_keeps_requiring_payment_when_type_stops(self):
        sub = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        self.type_a.payment_required = False
        self.type_a.save()
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_a), format="json"
        )
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_a, payment=CREDIT_CARD), format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertTrue(sub.payment_required)
        self.assertEqual(sub.payment["payment_type"], "Credit Card")

    def test_moving_to_a_type_that_requires_payment_demands_it(self):
        sub = make_submission(self.type_free)
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_a), format="json"
        )
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_a, payment=CREDIT_CARD), format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.type_id, self.type_a.id)
        self.assertTrue(sub.payment_required)
        self.assertEqual(sub.payment["payment_type"], "Credit Card")

    def test_moving_to_a_no_payment_type_drops_payment(self):
        sub = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        resp = self.as_user(self.lab_a_admin).put(
            self.url(sub), submission_payload(self.type_free, payment=CREDIT_CARD), format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.type_id, self.type_free.id)
        self.assertFalse(sub.payment_required)
        self.assertEqual(sub.payment, {})


class PluginValidatorTests(PaymentRequiredFixture):
    def test_validators_see_the_snapshotted_payment_arrangement(self):
        seen = []

        def validator(attrs, serializer):
            seen.append((serializer.payment_required, serializer.payment_type_id))

        validators = PluginManager().submission_validators
        validators["_payment_required_test"] = validator
        try:
            resp = self.as_anon().post(
                "/api/submissions/", submission_payload(self.type_free), format="json"
            )
            self.assertEqual(resp.status_code, 201, resp.content)
            resp = self.as_anon().post(
                "/api/submissions/", submission_payload(self.type_a, payment=CREDIT_CARD), format="json"
            )
            self.assertEqual(resp.status_code, 201, resp.content)
        finally:
            del validators["_payment_required_test"]
        # The fixture lab has no payment plugin, so the plugin id is None either way.
        self.assertEqual(seen, [(False, None), (True, None)])
