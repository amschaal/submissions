"""Locks in the endpoints that are PUBLIC BY DESIGN.

These assertions guard against an accidental future change that breaks
anonymous access to the public submission-tracking flow (an anonymous submitter
must be able to view / download / create / confirm a submission identified only
by its hard-to-guess 12-char id).  See the "submission-open-by-design" note.

If auth is ever *added* to these endpoints, these tests fail on purpose so the
change is a conscious decision rather than a silent regression.
"""
from django.core import mail

from dnaorder.tests.base import ApiTestCase


class PublicSubmissionAccessTests(ApiTestCase):
    def test_anonymous_can_retrieve_submission_detail(self):
        resp = self.as_anon().get("/api/submissions/{}/".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["id"], self.sub_a.id)

    def test_anonymous_can_retrieve_any_submission_regardless_of_lab(self):
        # detail queryset is Submission.objects.all() -- id is the capability.
        resp = self.as_anon().get("/api/submissions/{}/".format(self.sub_b.id))
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_anonymous_can_download_submission(self):
        resp = self.as_anon().get(
            "/api/submissions/{}/download/?format=csv".format(self.sub_a.id)
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn("attachment", resp.get("Content-Disposition", ""))

    def test_anonymous_create_is_permitted_at_auth_layer(self):
        # Permission layer must let anon through (public submission form). A bare
        # body then fails *validation* (400), never authorization (401/403).
        resp = self.as_anon().post("/api/submissions/", {}, format="json")
        self.assertEqual(resp.status_code, 400, resp.content)

    def test_anonymous_can_confirm_submission(self):
        before = len(mail.outbox)
        resp = self.as_anon().post(
            "/api/submissions/{}/confirm/".format(self.sub_a.id), {}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertIsNotNone(self.sub_a.confirmed)
        self.assertGreater(len(mail.outbox), before)

    def test_anonymous_can_cancel_unlocked_submission(self):
        resp = self.as_anon().post(
            "/api/submissions/{}/cancel/".format(self.sub_a.id), {}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertIsNotNone(self.sub_a.cancelled)

    def test_anonymous_cannot_cancel_locked_submission(self):
        # A locked submission may only be cancelled by lab staff.
        resp = self.as_anon().post(
            "/api/submissions/{}/cancel/".format(self.sub_a_locked.id), {}, format="json"
        )
        self.assertEqual(resp.status_code, 403, resp.content)
        self.sub_a_locked.refresh_from_db()
        self.assertIsNone(self.sub_a_locked.cancelled)


class PublicNotesTests(ApiTestCase):
    def setUp(self):
        from dnaorder.tests.base import make_note
        self.public_note = make_note(self.sub_a, "public", public=True)
        self.private_note = make_note(self.sub_a, "private", public=False)

    def test_anonymous_sees_only_public_notes(self):
        resp = self.as_anon().get("/api/notes/?submission={}".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        texts = {n["text"] for n in resp.data["results"]} if isinstance(resp.data, dict) else {n["text"] for n in resp.data}
        self.assertIn("public", texts)
        self.assertNotIn("private", texts)

    def test_notes_require_submission_param(self):
        # Without a submission id the queryset raises PermissionDenied by design.
        resp = self.as_anon().get("/api/notes/")
        self.assertEqual(resp.status_code, 403, resp.content)

    def test_lab_member_sees_private_notes(self):
        resp = self.as_user(self.lab_a_member).get(
            "/api/notes/?submission={}".format(self.sub_a.id)
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        texts = {n["text"] for n in (resp.data["results"] if isinstance(resp.data, dict) else resp.data)}
        self.assertIn("private", texts)


class PublicMetadataTests(ApiTestCase):
    """Read-only reference endpoints that the public submission form needs."""

    def test_default_institution_is_public(self):
        resp = self.as_anon().get("/api/institutions/default/")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_submission_types_are_publicly_listable(self):
        # SubmissionTypePermissions allows SAFE methods for everyone.
        resp = self.as_anon().get("/api/submission_types/")
        self.assertEqual(resp.status_code, 200, resp.content)
