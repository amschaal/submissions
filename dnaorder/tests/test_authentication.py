"""Authentication / authorization is enforced on protected endpoints.

Every test here asserts that a *protected* endpoint rejects callers who lack the
required identity or role, and accepts those who have it.  Endpoints that are
public by design are covered in ``test_open_endpoints.py`` instead.
"""
from dnaorder.tests.base import ApiTestCase


class SubmissionListAuthTests(ApiTestCase):
    def test_anonymous_cannot_list_submissions(self):
        self.assertDenied(self.as_anon().get("/api/submissions/"))

    def test_authenticated_user_can_list_but_sees_only_their_own(self):
        resp = self.as_user(self.outsider).get("/api/submissions/")
        self.assertEqual(resp.status_code, 200, resp.content)
        # outsider participates in / owns nothing -> empty page
        self.assertEqual(resp.data["count"], 0)

    def test_member_sees_lab_submissions_only_with_lab_param(self):
        resp = self.as_user(self.lab_a_member).get("/api/submissions/?lab=lab-a")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {row["id"] for row in resp.data["results"]}
        self.assertIn(self.sub_a.id, ids)
        self.assertNotIn(self.sub_b.id, ids)  # lab B never leaks into lab A


class UsersViewSetAuthTests(ApiTestCase):
    def test_anonymous_denied(self):
        self.assertDenied(self.as_anon().get("/api/users/"))

    def test_non_staff_denied(self):
        self.assertDenied(self.as_user(self.outsider).get("/api/users/"))

    def test_staff_allowed(self):
        resp = self.as_user(self.lab_a_member).get("/api/users/")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_user_detail_requires_staff(self):
        url = "/api/users/{}/".format(self.outsider.id)
        self.assertDenied(self.as_anon().get(url))
        self.assertDenied(self.as_user(self.outsider).get(url))
        self.assertEqual(self.as_user(self.lab_a_admin).get(url).status_code, 200)


class SubmissionStaffActionAuthTests(ApiTestCase):
    """detail=True staff actions must enforce lab membership at the object level."""

    LOCK = "/api/submissions/{}/lock/"
    STATUS = "/api/submissions/{}/update_status/"

    def test_lock_denied_to_anonymous(self):
        self.assertDenied(self.as_anon().post(self.LOCK.format(self.sub_a.id), {}, format="json"))

    def test_lock_denied_to_outsider(self):
        self.assertDenied(self.as_user(self.outsider).post(self.LOCK.format(self.sub_a.id), {}, format="json"))

    def test_lock_denied_across_labs(self):
        # A member of Lab B must not be able to act on a Lab A submission.
        self.assertDenied(
            self.as_user(self.lab_b_member).post(self.LOCK.format(self.sub_a.id), {}, format="json")
        )

    def test_lock_allowed_for_lab_member(self):
        resp = self.as_user(self.lab_a_member).post(self.LOCK.format(self.sub_a.id), {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_a.refresh_from_db()
        self.assertTrue(self.sub_a.locked)

    def test_update_status_requires_membership(self):
        body = {"status": "Received"}
        self.assertDenied(self.as_anon().post(self.STATUS.format(self.sub_a.id), body, format="json"))
        self.assertDenied(self.as_user(self.outsider).post(self.STATUS.format(self.sub_a.id), body, format="json"))
        ok = self.as_user(self.lab_a_admin).post(self.STATUS.format(self.sub_a.id), body, format="json")
        self.assertEqual(ok.status_code, 200, ok.content)


class SubmissionReportAuthTests(ApiTestCase):
    def test_reports_require_staff(self):
        self.assertDenied(self.as_anon().get("/api/submissions/reports/"))
        self.assertDenied(self.as_user(self.outsider).get("/api/submissions/reports/"))
        self.assertEqual(self.as_user(self.lab_a_member).get("/api/submissions/reports/").status_code, 200)


class InstitutionAuthTests(ApiTestCase):
    def test_list_requires_superuser(self):
        self.assertDenied(self.as_anon().get("/api/institutions/"))
        self.assertDenied(self.as_user(self.outsider).get("/api/institutions/"))
        self.assertDenied(self.as_user(self.inst_admin).get("/api/institutions/"))
        self.assertEqual(self.as_user(self.superuser).get("/api/institutions/").status_code, 200)

    def test_create_denied_to_non_superuser(self):
        body = {"id": "evil", "name": "Evil Inc"}
        self.assertDenied(self.as_anon().post("/api/institutions/", body, format="json"))
        self.assertDenied(self.as_user(self.inst_admin).post("/api/institutions/", body, format="json"))


class LabAdminActionAuthTests(ApiTestCase):
    def test_set_permissions_requires_lab_admin(self):
        url = "/api/labs/{}/set_permissions/".format(self.lab_a.lab_id)
        body = {"user_permissions": {}}
        self.assertDenied(self.as_anon().post(url, body, format="json"))
        self.assertDenied(self.as_user(self.outsider).post(url, body, format="json"))
        # A plain member (not admin) must not manage permissions.
        self.assertDenied(self.as_user(self.lab_a_member).post(url, body, format="json"))
        ok = self.as_user(self.lab_a_admin).post(url, body, format="json")
        self.assertEqual(ok.status_code, 200, ok.content)

    def test_toggle_disabled_requires_institution_admin(self):
        url = "/api/labs/{}/toggle_disabled/".format(self.lab_a.lab_id)
        self.assertDenied(self.as_anon().post(url, {}, format="json"))
        self.assertDenied(self.as_user(self.lab_a_member).post(url, {}, format="json"))
        ok = self.as_user(self.inst_admin).post(url, {}, format="json")
        self.assertEqual(ok.status_code, 200, ok.content)


class TokenEndpointAuthTests(ApiTestCase):
    def test_get_token_requires_staff(self):
        self.assertDenied(self.as_anon().get("/api/users/get_token/"))
        self.assertDenied(self.as_user(self.outsider).get("/api/users/get_token/"))
        self.assertEqual(self.as_user(self.lab_a_member).get("/api/users/get_token/").status_code, 200)

    def test_create_token_requires_staff(self):
        self.assertDenied(self.as_anon().post("/api/users/create_token/", {}, format="json"))
        resp = self.as_user(self.lab_a_member).post("/api/users/create_token/", {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertTrue(resp.data.get("token"))


class UserEmailAuthTests(ApiTestCase):
    def test_claim_requires_authentication(self):
        self.assertDenied(self.as_anon().post("/api/emails/claim/", {"email": "x@y.com"}, format="json"))

    def test_claim_allowed_for_authenticated_user(self):
        resp = self.as_user(self.outsider).post(
            "/api/emails/claim/", {"email": "new@example.com"}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
