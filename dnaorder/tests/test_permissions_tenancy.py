"""Multi-tenant isolation, IDOR, and permission-tier enforcement.

The app is multi-tenant by Institution/Lab.  These tests assert that a user's
reach is confined to labs they hold a permission on, and that the ADMIN /
MEMBER / ASSOCIATE tiers grant the rights they should (and no more).
"""
from dnaorder.tests.base import ApiTestCase, make_note


class SubmissionQuerysetIsolationTests(ApiTestCase):
    def test_member_cannot_pull_other_labs_submissions_via_lab_param(self):
        # Asking for a lab you have no permission on must NOT return its data;
        # the queryset silently falls back to "your own" submissions.
        resp = self.as_user(self.lab_a_member).get("/api/submissions/?lab=lab-b")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {row["id"] for row in resp.data["results"]}
        self.assertNotIn(self.sub_b.id, ids)

    def test_outsider_list_is_empty(self):
        resp = self.as_user(self.outsider).get("/api/submissions/")
        self.assertEqual(resp.data["count"], 0)

    def test_participant_sees_only_their_submission(self):
        from dnaorder.tests.base import make_participant
        make_participant(self.sub_b, self.outsider)
        resp = self.as_user(self.outsider).get("/api/submissions/")
        ids = {row["id"] for row in resp.data["results"]}
        self.assertEqual(ids, {self.sub_b.id})


class CrossLabActionTests(ApiTestCase):
    def test_lab_b_member_cannot_update_status_of_lab_a_submission(self):
        resp = self.as_user(self.lab_b_member).post(
            "/api/submissions/{}/update_status/".format(self.sub_a.id),
            {"status": "Received"}, format="json",
        )
        self.assertDenied(resp)

    def test_lab_b_member_cannot_lock_lab_a_submission(self):
        resp = self.as_user(self.lab_b_member).post(
            "/api/submissions/{}/lock/".format(self.sub_a.id), {}, format="json"
        )
        self.assertDenied(resp)


class PermissionTierTests(ApiTestCase):
    """ADMIN/MEMBER are lab members; ASSOCIATE is read-only and NOT a member."""

    def test_associate_can_view_lab_submissions(self):
        # Associate holds a LabPermission, so ?lab returns the lab's data.
        resp = self.as_user(self.lab_a_associate).get("/api/submissions/?lab=lab-a")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {row["id"] for row in resp.data["results"]}
        self.assertIn(self.sub_a.id, ids)

    def test_associate_cannot_perform_staff_actions(self):
        # is_lab_member() excludes ASSOCIATE, so IsLabMember-gated actions deny.
        resp = self.as_user(self.lab_a_associate).post(
            "/api/submissions/{}/lock/".format(self.sub_a.id), {}, format="json"
        )
        self.assertDenied(resp)

    def test_member_is_not_lab_admin(self):
        # Plain members cannot manage lab permissions (admin-only).
        resp = self.as_user(self.lab_a_member).post(
            "/api/labs/{}/set_permissions/".format(self.lab_a.lab_id),
            {"user_permissions": {}}, format="json",
        )
        self.assertDenied(resp)


class NoteIsolationTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.pub = make_note(self.sub_a, "pub-a", public=True)
        self.priv = make_note(self.sub_a, "priv-a", public=False)

    def test_other_lab_member_cannot_read_private_notes(self):
        resp = self.as_user(self.lab_b_member).get(
            "/api/notes/?submission={}".format(self.sub_a.id)
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        texts = {n["text"] for n in (resp.data["results"] if isinstance(resp.data, dict) else resp.data)}
        self.assertIn("pub-a", texts)
        self.assertNotIn("priv-a", texts)  # private note must not leak cross-lab


class SubmissionFileIsolationTests(ApiTestCase):
    def _make_file(self, submission):
        import tempfile
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        from dnaorder.models import SubmissionFile
        with override_settings(MEDIA_ROOT=tempfile.mkdtemp()):
            return SubmissionFile.objects.create(
                submission=submission,
                file=SimpleUploadedFile("data.txt", b"secret contents"),
            )

    def test_files_listable_by_submission_id_but_require_submission_param(self):
        # Listing without a submission id is denied (must scope to a submission).
        self.assertDenied(self.as_anon().get("/api/submission_files/"))

    def test_outsider_cannot_delete_file_of_locked_submission(self):
        f = self._make_file(self.sub_a_locked)
        resp = self.as_user(self.outsider).delete(
            "/api/submission_files/{}/?submission={}".format(f.id, self.sub_a_locked.id)
        )
        self.assertDenied(resp)
        from dnaorder.models import SubmissionFile
        self.assertTrue(SubmissionFile.objects.filter(id=f.id).exists())
