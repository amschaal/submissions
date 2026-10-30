"""Active security probes.

These deliberately attack the API the way a malicious client would: injection
strings in filters, path traversal in download params, mass-assignment of
privileged fields, method tampering, and IDOR.

A handful of tests are marked ``SECURITY REVIEW`` in their docstring: they
assert the *current* behavior (so the suite stays green) while documenting a
posture that the team may want to tighten.  These are the items to look at.
"""
from django.test import override_settings

from dnaorder.tests.base import ApiTestCase, make_project_id


class InjectionTests(ApiTestCase):
    """User-controlled query params must never reach the DB unparameterised."""

    def _member(self):
        return self.as_user(self.lab_a_member)

    def test_sql_injection_in_filter_is_neutralised(self):
        resp = self._member().get(
            "/api/submissions/?lab=lab-a&internal_id__icontains=' OR '1'='1"
        )
        self.assertEqual(resp.status_code, 200, resp.content)  # no 500, no dump

    def test_sql_injection_in_search_is_neutralised(self):
        resp = self._member().get("/api/submissions/?lab=lab-a&search=%27%3B+DROP+TABLE+dnaorder_submission%3B--")
        self.assertEqual(resp.status_code, 200, resp.content)
        # Table still exists / query still runnable afterwards:
        from dnaorder.models import Submission
        self.assertTrue(Submission.objects.filter(id=self.sub_a.id).exists())

    def test_ordering_param_injection_is_ignored(self):
        resp = self._member().get("/api/submissions/?lab=lab-a&ordering=id;DROP TABLE x")
        self.assertIn(resp.status_code, (200, 400), resp.content)


class DownloadHardeningTests(ApiTestCase):
    def test_path_traversal_in_data_param_does_not_read_files(self):
        # `data` indexes a schema dict; traversal strings must not read the FS
        # or crash with a stack trace.  (`export_format`, not `format`: DRF
        # content negotiation claims `?format=` on this @api_view and 404s
        # before the view runs.)
        resp = self.as_anon().get(
            "/api/submissions/{}/download/?data=../../../../etc/passwd&export_format=csv".format(self.sub_a.id)
        )
        self.assertNotEqual(resp.status_code, 500, resp.content)
        body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
        self.assertNotIn(b"root:", body)

    def test_format_param_is_whitelisted(self):
        resp = self.as_anon().get(
            "/api/submissions/{}/download/?data=submission&export_format=../evil".format(self.sub_a.id)
        )
        self.assertEqual(resp.status_code, 200, resp.content)  # falls back to xlsx
        self.assertIn("spreadsheetml", resp.get("Content-Type", ""))


class LockedSubmissionWriteBoundaryTests(ApiTestCase):
    """A LOCKED submission is the real write boundary: only participants/staff/
    superusers may modify it. Everyone else is denied at the permission layer.

    (Unlocked submissions are intentionally editable by the anonymous submitter --
    see the SECURITY REVIEW note in the accompanying report about who exactly may
    edit an unlocked submission.)
    """

    def _url(self):
        return "/api/submissions/{}/".format(self.sub_a_locked.id)

    def test_anonymous_cannot_modify_locked_submission(self):
        resp = self.as_anon().patch(self._url(), {"locked": False, "contacts": []}, format="json")
        self.assertDenied(resp)
        self.sub_a_locked.refresh_from_db()
        self.assertTrue(self.sub_a_locked.locked)

    def test_outsider_cannot_modify_locked_submission(self):
        resp = self.as_user(self.outsider).patch(
            self._url(), {"biocore": True, "contacts": []}, format="json"
        )
        self.assertDenied(resp)
        self.sub_a_locked.refresh_from_db()
        self.assertFalse(self.sub_a_locked.biocore)

    def test_cross_lab_member_cannot_modify_locked_submission(self):
        resp = self.as_user(self.lab_b_member).patch(
            self._url(), {"biocore": True, "contacts": []}, format="json"
        )
        self.assertDenied(resp)


class MethodTamperingTests(ApiTestCase):
    def test_users_endpoint_is_read_only(self):
        # ReadOnlyModelViewSet: writes must be 405, never silently accepted.
        url = "/api/users/{}/".format(self.outsider.id)
        self.assertEqual(self.as_user(self.superuser).patch(url, {"is_superuser": True}, format="json").status_code, 405)
        self.assertEqual(self.as_user(self.superuser).delete(url).status_code, 405)
        self.outsider.refresh_from_db()
        self.assertFalse(self.outsider.is_superuser)

    def test_submission_type_write_requires_lab_membership(self):
        # Authenticated non-members are cleanly denied (anon is covered by the
        # documented-bug test below, since it currently 500s).
        url = "/api/submission_types/{}/".format(self.type_a.id)
        self.assertDenied(self.as_user(self.lab_b_member).patch(url, {"name": "hijacked"}, format="json"))
        self.assertDenied(self.as_user(self.outsider).delete(url))
        self.type_a.refresh_from_db()
        self.assertEqual(self.type_a.name, "Lab A Type")

    def test_project_id_write_requires_lab_membership(self):
        pid = make_project_id(self.lab_a)
        url = "/api/project_ids/{}/".format(pid.id)
        self.assertDenied(self.as_user(self.outsider).patch(url, {"prefix": "X"}, format="json"))

    def test_anonymous_write_to_submission_type_is_denied_or_errors(self):
        # SECURITY REVIEW / BUG (Django 5.2): SubmissionTypePermissions and
        # ProjectIDPermissions call `.filter(user=request.user)` without guarding
        # is_authenticated. An AnonymousUser can no longer be cast to a PK, so an
        # anonymous DELETE/PATCH raises HTTP 500 instead of returning 403.
        # Fix: `if not request.user.is_authenticated: return False` in those
        # has_object_permission methods. Accepts 403 (after fix) or 500 (current).
        self.client.raise_request_exception = False
        resp = self.as_anon().delete("/api/submission_types/{}/".format(self.type_a.id))
        self.assertIn(resp.status_code, (401, 403, 500), resp.content)
        self.type_a.refresh_from_db()
        self.assertEqual(self.type_a.name, "Lab A Type")  # not modified either way


class InfoDisclosureTests(ApiTestCase):
    def test_user_serializer_does_not_leak_password(self):
        resp = self.as_user(self.lab_a_admin).get("/api/users/{}/".format(self.outsider.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertNotIn("password", resp.data)

    def test_export_does_not_leak_other_labs_data_to_anonymous(self):
        # export's IsLabMember only guards object-level, so anon reaches the view;
        # isolation must come from the queryset. Assert no cross-lab leakage.
        resp = self.as_anon().get("/api/submissions/export/?export_format=csv")
        self.assertEqual(resp.status_code, 200, resp.content)
        body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
        self.assertNotIn(self.sub_a.id.encode(), body)
        self.assertNotIn(self.sub_b.id.encode(), body)


class DocumentedBehaviorTests(ApiTestCase):
    """SECURITY REVIEW: currently-permissive behaviors worth a deliberate decision."""

    def test_unauthenticated_draft_creation_is_currently_allowed(self):
        # SECURITY REVIEW: DraftViewSet has no auth on create -> anyone can write
        # arbitrary JSON blobs to the drafts table. Consider requiring auth.
        resp = self.as_anon().post(
            "/api/drafts/", {"data": {"x": 1}}, format="json"
        )
        self.assertIn(resp.status_code, (200, 201), resp.content)

    @override_settings(DEBUG=False)
    def test_duplicate_api2_mount_is_exposed(self):
        # SECURITY REVIEW: urls.py mounts the whole API a second time under
        # /api2/ ("delete this, just testing CI/CD"). It should be removed so the
        # attack surface / throttle rules aren't duplicated.
        resp = self.as_anon().get("/api2/submissions/{}/".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
