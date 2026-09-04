"""SubmissionType.payment_required and how it applies to submissions.

Payment is only displayed and validated when required, and the rule is data
driven: payment already captured on a submission is never thrown away (it
stays shown, validated and editable with its stored payment plugin), and
otherwise the submission's current type decides whether payment is collected
at all.  Moving a submission to a different type simply applies that type's
requirement to a submission that has no payment yet.  Payment that was
validated when captured is not validated or rewritten again unless the client
actually changes it (KeepValidatedPaymentTests).

The fixture labs have no payment plugin configured, so the default UC Davis
payment serializer applies whenever payment is required.
"""
from dnaorder.models import Submission
from dnaorder.tests.base import ApiTestCase, make_submission, make_submission_type
from plugins import PluginManager

#: Minimal valid payment for the default (UCD) payment serializer.
CREDIT_CARD = {"payment_type": "Credit Card", "payment_info": ""}
#: Valid when it was captured, invalid under today's UCD account rules.
STALE_ACCOUNT = {"payment_type": "DaFIS", "payment_info": "3-OLDSTYLE"}


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

    def put(self, submission, payload):
        return self.as_user(self.lab_a_admin).put(self.url(submission), payload, format="json")


class SubmissionTypePaymentRequiredTests(PaymentRequiredFixture):
    def test_defaults_to_required(self):
        self.assertTrue(self.type_a.payment_required)

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


class EffectiveRequirementTests(PaymentRequiredFixture):
    """Submission.payment_required: payment on record wins, else the type decides."""

    def test_unpaid_submission_follows_its_type(self):
        self.assertTrue(make_submission(self.type_a).payment_required)
        self.assertFalse(make_submission(self.type_free).payment_required)

    def test_paid_submission_requires_payment_whatever_its_type_says(self):
        sub = make_submission(self.type_free, payment=dict(CREDIT_CARD))
        self.assertTrue(sub.has_payment)
        self.assertTrue(sub.payment_required)

    def test_toggling_the_type_changes_unpaid_submissions_only(self):
        unpaid = make_submission(self.type_a)
        paid = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        self.type_a.payment_required = False
        self.type_a.save()
        unpaid.refresh_from_db()
        paid.refresh_from_db()
        self.assertFalse(unpaid.payment_required)
        self.assertTrue(paid.payment_required)


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
        self.assertEqual(sub.payment["payment_type"], "Credit Card")
        self.assertIs(resp.data["payment_required"], True)

    def test_no_payment_needed_when_type_does_not_require_it(self):
        resp = self.as_anon().post("/api/submissions/", submission_payload(self.type_free), format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        sub = Submission.objects.get(pk=resp.data["id"])
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

    def test_payment_required_in_response_is_derived_not_posted(self):
        payload = submission_payload(self.type_a, payment=CREDIT_CARD, payment_required=False)
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertIs(resp.data["payment_required"], True)

        payload = submission_payload(self.type_free, payment_required=True)
        resp = self.as_anon().post("/api/submissions/", payload, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertIs(resp.data["payment_required"], False)


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

    def test_paid_submission_returns_display_and_stays_required(self):
        sub = make_submission(self.type_free, payment=dict(CREDIT_CARD))
        detail = self.as_user(self.lab_a_member).get(self.url(sub))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["payment_required"], True)
        self.assertEqual(detail.data["payment"]["display"]["Payment Type"], "Credit Card")

    def test_unpaid_submission_of_a_paying_type_is_required_but_empty(self):
        # e.g. a submission that predates payment tracking.
        detail = self.as_user(self.lab_a_member).get(self.url(self.sub_a))
        self.assertEqual(detail.status_code, 200, detail.content)
        self.assertIs(detail.data["payment_required"], True)
        self.assertEqual(detail.data["payment"], {})


class UpdateSubmissionPaymentTests(PaymentRequiredFixture):
    def test_paid_submission_keeps_its_payment_when_type_stops_requiring_it(self):
        sub = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        self.type_a.payment_required = False
        self.type_a.save()
        # Editing without touching payment keeps it; changing it still validates it.
        resp = self.put(sub, submission_payload(self.type_a))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIs(resp.data["payment_required"], True)
        sub.refresh_from_db()
        self.assertEqual(sub.payment["payment_type"], "Credit Card")
        resp = self.put(sub, submission_payload(
            self.type_a, payment={"payment_type": "DaFIS", "payment_info": "bad"}
        ))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)

    def test_unpaid_submission_needs_nothing_while_type_does_not_require_payment(self):
        sub = make_submission(self.type_free)
        resp = self.put(sub, submission_payload(self.type_free, payment=CREDIT_CARD))
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.payment, {})

    def test_unpaid_submission_follows_type_when_it_starts_requiring_payment(self):
        sub = make_submission(self.type_free)
        self.type_free.payment_required = True
        self.type_free.save()
        resp = self.put(sub, submission_payload(self.type_free))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)
        resp = self.put(sub, submission_payload(self.type_free, payment=CREDIT_CARD))
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.payment["payment_type"], "Credit Card")

    def test_moving_unpaid_submission_to_a_type_that_requires_payment_demands_it(self):
        sub = make_submission(self.type_free)
        resp = self.put(sub, submission_payload(self.type_a))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)
        resp = self.put(sub, submission_payload(self.type_a, payment=CREDIT_CARD))
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.type_id, self.type_a.id)
        self.assertEqual(sub.payment["payment_type"], "Credit Card")

    def test_moving_unpaid_submission_to_a_no_payment_type_needs_nothing(self):
        sub = make_submission(self.type_a)
        resp = self.put(sub, submission_payload(self.type_free))
        self.assertEqual(resp.status_code, 200, resp.content)
        sub.refresh_from_db()
        self.assertEqual(sub.type_id, self.type_free.id)
        self.assertEqual(sub.payment, {})

    def test_moving_paid_submission_to_a_no_payment_type_keeps_its_payment(self):
        sub = make_submission(self.type_a, payment=dict(CREDIT_CARD))
        resp = self.put(sub, submission_payload(self.type_free))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIs(resp.data["payment_required"], True)
        sub.refresh_from_db()
        self.assertEqual(sub.type_id, self.type_free.id)
        self.assertEqual(sub.payment["payment_type"], "Credit Card")


class KeepValidatedPaymentTests(PaymentRequiredFixture):
    """Payment that was validated when captured is neither validated again nor
    rewritten unless the client actually changes it."""

    def setUp(self):
        super().setUp()
        self.sub = make_submission(self.type_a, payment=dict(STALE_ACCOUNT))

    def assertPaymentKept(self, resp):
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.payment, STALE_ACCOUNT)

    def test_omitted_payment_is_kept(self):
        self.assertPaymentKept(self.put(self.sub, submission_payload(self.type_a)))

    def test_emptied_payment_is_kept(self):
        self.assertPaymentKept(self.put(self.sub, submission_payload(self.type_a, payment={})))

    def test_round_tripped_payment_is_kept_without_revalidation(self):
        # What the form does: send back exactly what the API gave it, derived
        # display included.  A stale account string must not block the edit.
        given = self.as_user(self.lab_a_admin).get(self.url(self.sub)).data["payment"]
        self.assertIn("display", given)
        self.assertPaymentKept(self.put(self.sub, submission_payload(self.type_a, payment=given)))

    def test_derived_fields_are_ignored_when_comparing(self):
        payload = submission_payload(
            self.type_a, payment=dict(STALE_ACCOUNT, display={"anything": "else"})
        )
        self.assertPaymentKept(self.put(self.sub, payload))

    def test_changed_payment_is_validated(self):
        resp = self.put(self.sub, submission_payload(
            self.type_a, payment={"payment_type": "DaFIS", "payment_info": "still-bad"}
        ))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment_info", resp.data["payment"])
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.payment, STALE_ACCOUNT)

    def test_changed_payment_is_stored_when_valid(self):
        resp = self.put(self.sub, submission_payload(self.type_a, payment=CREDIT_CARD))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.payment["payment_type"], "Credit Card")

    def test_unpaid_submission_still_needs_payment(self):
        # Nothing to keep: a paying type's submission without payment must supply it.
        resp = self.put(self.sub_a, submission_payload(self.type_a))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment", resp.data)


class PluginValidatorTests(PaymentRequiredFixture):
    def test_validators_see_the_effective_payment_arrangement(self):
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
