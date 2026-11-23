"""Next to nothing is available without signing in.

The only endpoints an anonymous browser can use are the ones the app needs to
show its landing pages (the institution, and each lab's name and welcome text)
and to sign in.  Everything else must refuse an anonymous request (401/403),
whatever ids it carries.

``AnonymousSweepTests`` walks every route the API routers register, so an
endpoint added later is covered without anyone remembering to add it here.
"""
import re

from django.urls import Resolver404, resolve

from billing.api.urls import router as billing_router
from dnaorder.api.urls import router as api_router
from dnaorder.tests.base import ApiTestCase, make_lab, make_note

#: Reachable while signed out.
PUBLIC_PATHS = {
    "/api/institutions/default/",  # the site landing page, and branding for the sign-in page
    "/api/public/labs/",  # the labs listed on the site landing page
    "/api/public/labs/000000000000/",  # a lab's landing page
}

#: An id that matches every lookup pattern but no object.
DUMMY_ID = "000000000000"


class PublicLandingPageTests(ApiTestCase):
    """dnaorder/api/public.py: a lab's name and welcome text, and nothing more."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.lab_a.home_page = "<p>Welcome to Lab A</p>"
        cls.lab_a.save()
        cls.lab_off = make_lab(cls.institution, lab_id="lab-off", name="Disabled Lab")
        cls.lab_off.disabled = True
        cls.lab_off.save()

    def test_anyone_can_list_enabled_labs_by_name(self):
        resp = self.as_anon().get("/api/public/labs/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data, [
            {"lab_id": "lab-a", "name": "Lab A"},
            {"lab_id": "lab-b", "name": "Lab B"},
        ])

    def test_anyone_can_read_a_labs_landing_page(self):
        resp = self.as_anon().get("/api/public/labs/lab-a/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data, {"lab_id": "lab-a", "name": "Lab A", "home_page": "<p>Welcome to Lab A</p>"})

    def test_signed_in_users_get_the_same_limited_view(self):
        for user in [self.outsider, self.lab_a_admin, self.superuser]:
            resp = self.as_user(user).get("/api/public/labs/lab-a/")
            self.assertEqual(set(resp.data), {"lab_id", "name", "home_page"}, user.username)

    def test_disabled_or_unknown_labs_are_not_found(self):
        for client in (self.as_anon, lambda: self.as_user(self.superuser)):
            self.assertEqual(client().get("/api/public/labs/lab-off/").status_code, 404)
            self.assertEqual(client().get("/api/public/labs/no-such-lab/").status_code, 404)

    def test_public_view_is_read_only(self):
        for client in (self.as_anon, lambda: self.as_user(self.superuser)):
            self.assertEqual(client().post("/api/public/labs/", {"name": "x", "lab_id": "x"}, format="json").status_code, 405)
            for method in ("put", "patch", "delete"):
                resp = getattr(client(), method)("/api/public/labs/lab-a/", {"name": "Renamed"}, format="json")
                self.assertEqual(resp.status_code, 405, method)
        self.lab_a.refresh_from_db()
        self.assertEqual(self.lab_a.name, "Lab A")

    def test_full_lab_endpoints_still_need_sign_in(self):
        self.assertDenied(self.as_anon().get("/api/labs/"))
        self.assertDenied(self.as_anon().get("/api/labs/lab-a/"))


class PublicEndpointTests(ApiTestCase):
    def test_default_institution_is_public(self):
        resp = self.as_anon().get("/api/institutions/default/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["id"], self.institution.id)

    def test_get_user_tells_an_anonymous_browser_it_is_signed_out(self):
        # Also the call that hands the browser its CSRF cookie.
        resp = self.as_anon().get("/api/get_user/")
        self.assertEqual(resp.status_code, 403, resp.content)
        self.assertIn("csrftoken", resp.cookies)

    def test_sign_in_code_can_be_requested(self):
        resp = self.as_anon().post(
            "/_allauth/browser/v1/auth/code/request", {"email": "someone@example.com"}, format="json"
        )
        self.assertEqual(resp.status_code, 401, resp.content)  # "code sent, now confirm it"


class AnonymousSubmissionTests(ApiTestCase):
    """The submission id in a link is not a credential."""

    def test_submission_cannot_be_read(self):
        for submission in [self.sub_a, self.sub_a_locked, self.sub_b]:
            self.assertDenied(self.as_anon().get("/api/submissions/{}/".format(submission.id)))

    def test_submission_cannot_be_downloaded(self):
        resp = self.as_anon().get(
            "/api/submissions/{}/download/?data=submission&export_format=csv".format(self.sub_a.id)
        )
        self.assertDenied(resp)
        self.assertNotIn("attachment", resp.get("Content-Disposition", ""))

    def test_submission_cannot_be_created(self):
        from dnaorder.models import Submission
        from dnaorder.tests.test_payment_required import submission_payload
        before = Submission.objects.count()
        self.assertDenied(self.as_anon().post("/api/submissions/", {}, format="json"))
        self.assertDenied(self.as_anon().post("/api/submissions/", submission_payload(self.type_a), format="json"))
        self.assertEqual(Submission.objects.count(), before)

    def test_submission_cannot_be_changed_cancelled_confirmed_or_deleted(self):
        from dnaorder.models import Submission
        url = "/api/submissions/{}/".format(self.sub_a.id)
        self.assertDenied(self.as_anon().patch(url, {"comments": "x", "contacts": []}, format="json"))
        self.assertDenied(self.as_anon().post(url + "cancel/", {}, format="json"))
        self.assertDenied(self.as_anon().post(url + "confirm/", {}, format="json"))
        self.assertDenied(self.as_anon().delete(url))
        submission = Submission.objects.get(pk=self.sub_a.pk)
        self.assertIsNone(submission.cancelled)
        self.assertIsNone(submission.confirmed)

    def test_notes_and_files_cannot_be_read_or_added(self):
        make_note(self.sub_a, "public", public=True)
        self.assertDenied(self.as_anon().get("/api/notes/?submission={}".format(self.sub_a.id)))
        self.assertDenied(self.as_anon().get("/api/submission_files/?submission={}".format(self.sub_a.id)))
        self.assertDenied(self.as_anon().post(
            "/api/notes/", {"submission": self.sub_a.id, "text": "hello", "type": "NOTE"}, format="json"
        ))

    def test_drafts_and_imports_are_closed(self):
        self.assertDenied(self.as_anon().post("/api/drafts/", {"data": {"x": 1}}, format="json"))
        self.assertDenied(self.as_anon().get("/api/imports/"))
        url = "/submissions/{}".format(self.sub_a.id)
        self.assertDenied(self.as_anon().get("/api/imports/get_submission/?url=" + url))
        self.assertDenied(self.as_anon().post("/api/tables/template/", {"submission": self.sub_a.id, "table": "samples"}, format="json"))

    def test_reference_data_is_closed(self):
        for path in ["/api/submission_types/", "/api/labs/", "/api/labs/lab-a/", "/api/validators/",
                     "/api/vocabularies/", "/api/plugins/", "/api/billing/services/", "/api/project_ids/"]:
            self.assertDenied(self.as_anon().get(path), path)


def _fill(pattern):
    """Turn a route regex into a concrete path: every (group) becomes a dummy id."""
    while True:
        filled = re.sub(r"\([^()]*\)", DUMMY_ID, pattern)
        if filled == pattern:
            return filled
        pattern = filled


def router_paths(prefix, router):
    """A list and a detail path for every viewset, plus one for each extra action."""
    paths = set()
    for route_prefix, viewset, _basename in router.registry:
        base = "{}{}/".format(prefix, _fill(route_prefix))
        paths.update([base, "{}{}/".format(base, DUMMY_ID)])
        for action in viewset.get_extra_actions():
            url_path = _fill(action.url_path)
            if action.detail:
                paths.add("{}{}/{}/".format(base, DUMMY_ID, url_path))
            else:
                paths.add("{}{}/".format(base, url_path))
    return paths


class AnonymousSweepTests(ApiTestCase):
    def all_paths(self):
        paths = router_paths("/api/", api_router) | router_paths("/api/billing/", billing_router)
        paths.update([
            "/api/submissions/{}/download/".format(DUMMY_ID),
            "/api/validate/",
            "/api/logout/",
        ])
        resolvable = set()
        for path in paths:
            try:
                resolve(path)
            except Resolver404:
                continue  # a pattern the dummy id can't satisfy (e.g. a fixed choice)
            resolvable.add(path)
        return resolvable - PUBLIC_PATHS

    def test_sweep_covers_the_api(self):
        paths = self.all_paths()
        self.assertGreater(len(paths), 60, sorted(paths))
        for expected in ["/api/submissions/", "/api/submissions/{}/".format(DUMMY_ID), "/api/drafts/",
                         "/api/submission_files/field_upload/", "/api/imports/get_submission/",
                         "/api/tables/template/", "/api/billing/services/", "/api/emails/claim/"]:
            self.assertIn(expected, paths)

    def test_every_endpoint_refuses_anonymous_requests(self):
        client = self.as_anon()
        for path in sorted(self.all_paths()):
            for method in ("get", "post"):
                with self.subTest(path=path, method=method):
                    resp = getattr(client, method)(path, {}, format="json") if method == "post" else client.get(path)
                    self.assertIn(
                        resp.status_code, (401, 403),
                        "{} {} -> {}".format(method.upper(), path, resp.status_code),
                    )
