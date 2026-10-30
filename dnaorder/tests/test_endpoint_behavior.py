"""Happy-path behavior: endpoints return the right data and mutate correctly."""
from django.core import mail

from dnaorder.models import Note, Submission
from dnaorder.tests.base import ApiTestCase


class SubmissionListingBehaviorTests(ApiTestCase):
    def test_list_is_paginated(self):
        resp = self.as_user(self.lab_a_member).get("/api/submissions/?lab=lab-a")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn("count", resp.data)
        self.assertIn("results", resp.data)
        self.assertGreaterEqual(resp.data["count"], 2)  # sub_a + sub_a_locked

    def test_exact_id_filter(self):
        # django-filter maps the `exact` lookup to the bare field name (`id`),
        # not `id__exact`.
        resp = self.as_user(self.lab_a_member).get(
            "/api/submissions/?lab=lab-a&id={}".format(self.sub_a.id)
        )
        ids = {r["id"] for r in resp.data["results"]}
        self.assertEqual(ids, {self.sub_a.id})

    def test_search_matches_first_name(self):
        resp = self.as_user(self.lab_a_member).get("/api/submissions/?lab=lab-a&search=Alpha")
        ids = {r["id"] for r in resp.data["results"]}
        self.assertIn(self.sub_a.id, ids)

    def test_detail_exposes_expected_fields(self):
        resp = self.as_user(self.lab_a_member).get("/api/submissions/{}/".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        for field in ("id", "status", "editable"):
            self.assertIn(field, resp.data)


class SubmissionMutationBehaviorTests(ApiTestCase):
    def test_update_status_sets_status_and_logs_note(self):
        before = Note.objects.filter(submission=self.sub_a).count()
        resp = self.as_user(self.lab_a_admin).post(
            "/api/submissions/{}/update_status/".format(self.sub_a.id),
            {"status": "In Progress"}, format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertEqual(self.sub_a.status, "In Progress")
        self.assertEqual(Note.objects.filter(submission=self.sub_a).count(), before + 1)
        self.assertIn("status_updates", self.sub_a.data)

    def test_update_status_with_email_notifies_submitter(self):
        before = len(mail.outbox)
        self.as_user(self.lab_a_admin).post(
            "/api/submissions/{}/update_status/".format(self.sub_a.id),
            {"status": "Done", "email": True}, format="json",
        )
        self.assertGreater(len(mail.outbox), before)

    def test_lock_then_unlock(self):
        base = "/api/submissions/{}/".format(self.sub_a.id)
        self.as_user(self.lab_a_admin).post(base + "lock/", {}, format="json")
        self.sub_a.refresh_from_db()
        self.assertTrue(self.sub_a.locked)
        self.as_user(self.lab_a_admin).post(base + "unlock/", {}, format="json")
        self.sub_a.refresh_from_db()
        self.assertFalse(self.sub_a.locked)

    def test_cancel_marks_submission_cancelled(self):
        resp = self.as_user(self.lab_a_admin).post(
            "/api/submissions/{}/cancel/".format(self.sub_a.id), {}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertIsNotNone(self.sub_a.cancelled)

    def test_samples_received_records_date_and_receiver(self):
        resp = self.as_user(self.lab_a_member).post(
            "/api/submissions/{}/samples_received/".format(self.sub_a.id), {}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertIsNotNone(self.sub_a.samples_received)
        self.assertEqual(self.sub_a.received_by_id, self.lab_a_member.id)


class ReferenceEndpointBehaviorTests(ApiTestCase):
    def test_default_institution_returns_current_site_institution(self):
        resp = self.as_anon().get("/api/institutions/default/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["id"], self.institution.id)

    def test_submission_types_listable_and_retrievable(self):
        listing = self.as_anon().get("/api/submission_types/")
        self.assertEqual(listing.status_code, 200, listing.content)
        detail = self.as_anon().get("/api/submission_types/{}/".format(self.type_a.id))
        self.assertEqual(detail.status_code, 200, detail.content)

    def test_staff_can_search_users_by_email(self):
        resp = self.as_user(self.lab_a_admin).get("/api/users/?search=out@example.com")
        self.assertEqual(resp.status_code, 200, resp.content)
        usernames = {u["username"] for u in resp.data["results"]}
        self.assertIn("outsider", usernames)


class ExportBehaviorTests(ApiTestCase):
    def test_member_export_contains_own_lab_and_excludes_others(self):
        resp = self.as_user(self.lab_a_member).get(
            "/api/submissions/export/?lab=lab-a&export_format=csv"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
        self.assertIn(self.sub_a.id.encode(), body)
        self.assertNotIn(self.sub_b.id.encode(), body)
