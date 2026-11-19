"""Active security probes.

These deliberately attack the API the way a malicious client would: injection
strings in filters, path traversal in download params, mass-assignment of
privileged fields, method tampering, and IDOR.

"""
from dnaorder.models import Draft, ProjectID, SubmissionType
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
        resp = self.as_submitter().get(
            "/api/submissions/{}/download/?data=../../../../etc/passwd&export_format=csv".format(self.sub_a.id)
        )
        self.assertNotEqual(resp.status_code, 500, resp.content)
        body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
        self.assertNotIn(b"root:", body)

    def test_format_param_is_whitelisted(self):
        resp = self.as_submitter().get(
            "/api/submissions/{}/download/?data=submission&export_format=../evil".format(self.sub_a.id)
        )
        self.assertEqual(resp.status_code, 200, resp.content)  # falls back to xlsx
        self.assertIn("spreadsheetml", resp.get("Content-Type", ""))


class LockedSubmissionWriteBoundaryTests(ApiTestCase):
    """Once a submission is locked only participants and superusers may modify it.
    The people it names can still read it; everyone else can't reach it at all.
    """

    def _url(self):
        return "/api/submissions/{}/".format(self.sub_a_locked.id)

    def test_anonymous_cannot_modify_locked_submission(self):
        resp = self.as_anon().patch(self._url(), {"locked": False, "contacts": []}, format="json")
        self.assertDenied(resp)
        self.sub_a_locked.refresh_from_db()
        self.assertTrue(self.sub_a_locked.locked)

    def test_named_submitter_cannot_modify_locked_submission(self):
        resp = self.as_submitter().patch(self._url(), {"biocore": True, "contacts": []}, format="json")
        self.assertEqual(resp.status_code, 403, resp.content)
        self.sub_a_locked.refresh_from_db()
        self.assertFalse(self.sub_a_locked.biocore)
        self.assertEqual(self.as_submitter().get(self._url()).status_code, 200)

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
        url = "/api/submission_types/{}/".format(self.type_a.id)
        self.assertDenied(self.as_user(self.lab_b_member).patch(url, {"name": "hijacked"}, format="json"))
        self.assertDenied(self.as_user(self.outsider).delete(url))
        self.type_a.refresh_from_db()
        self.assertEqual(self.type_a.name, "Lab A Type")

    def test_project_id_write_requires_lab_membership(self):
        pid = make_project_id(self.lab_a)
        url = "/api/project_ids/{}/".format(pid.id)
        self.assertDenied(self.as_user(self.outsider).patch(url, {"prefix": "X"}, format="json"))

    def test_anonymous_write_to_submission_type_is_denied(self):
        url = "/api/submission_types/{}/".format(self.type_a.id)
        self.assertDenied(self.as_anon().delete(url))
        self.assertDenied(self.as_anon().patch(url, {"name": "hijacked"}, format="json"))
        self.type_a.refresh_from_db()
        self.assertEqual(self.type_a.name, "Lab A Type")

    def test_only_lab_staff_can_create_submission_types(self):
        body = {"lab": self.lab_a.id, "name": "Injected"}
        for client in (self.as_anon, self.as_submitter):
            self.assertDenied(client().post("/api/submission_types/", body, format="json"))
        for user in [self.outsider, self.lab_b_member, self.lab_a_associate]:
            self.assertDenied(self.as_user(user).post("/api/submission_types/", body, format="json"), user.username)
        self.assertFalse(SubmissionType.objects.filter(name="Injected").exists())
        resp = self.as_user(self.lab_a_member).post("/api/submission_types/", body, format="json")
        self.assertNotIn(resp.status_code, (401, 403, 404), resp.content)

    def test_only_lab_staff_can_use_project_ids(self):
        pid = make_project_id(self.lab_a)
        body = {"lab": self.lab_a.id, "prefix": "INJ"}
        for user in [None, self.submitter, self.outsider, self.lab_b_member]:
            client = self.as_user(user)
            self.assertDenied(client.post("/api/project_ids/", body, format="json"), user)
            self.assertDenied(client.get("/api/project_ids/{}/".format(pid.id)), user)
        self.assertFalse(ProjectID.objects.filter(prefix="INJ").exists())
        # Lab B staff may use the endpoint, but never see Lab A's prefixes.
        listing = self.as_user(self.lab_b_member).get("/api/project_ids/")
        self.assertEqual(listing.status_code, 200, listing.content)
        rows = listing.data["results"] if isinstance(listing.data, dict) else listing.data
        self.assertEqual(rows, [])
        self.assertEqual(self.as_user(self.lab_a_member).get("/api/project_ids/{}/".format(pid.id)).status_code, 200)


class InfoDisclosureTests(ApiTestCase):
    def test_user_serializer_does_not_leak_password(self):
        resp = self.as_user(self.lab_a_admin).get("/api/users/{}/".format(self.outsider.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertNotIn("password", resp.data)

    def test_export_only_contains_what_the_user_can_list(self):
        self.assertDenied(self.as_anon().get("/api/submissions/export/?export_format=csv"))
        # Asking for a lab you hold no permission in does not widen the export.
        for path in ["/api/submissions/export/?export_format=csv", "/api/submissions/export/?lab=lab-a&export_format=csv"]:
            resp = self.as_user(self.outsider).get(path)
            self.assertEqual(resp.status_code, 200, resp.content)
            body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
            self.assertNotIn(self.sub_a.id.encode(), body)
            self.assertNotIn(self.sub_b.id.encode(), body)
        resp = self.as_user(self.contact_user).get("/api/submissions/export/?export_format=csv")
        body = resp.getvalue() if hasattr(resp, "getvalue") else resp.content
        self.assertIn(self.sub_a.id.encode(), body)      # a contact on sub_a only
        self.assertNotIn(self.sub_b.id.encode(), body)

    def test_drafts_cannot_be_listed_or_deleted(self):
        # Drafts hold whole form submissions (contacts, file field upload ids), so
        # they are only reachable by id, by the people entitled to them.
        resp = self.as_user(self.outsider).post("/api/drafts/", {"data": {"x": 1}}, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        draft_id = resp.data["id"]
        self.assertEqual(self.as_user(self.outsider).get("/api/drafts/").status_code, 405)
        self.assertEqual(self.as_user(self.superuser).get("/api/drafts/").status_code, 405)
        self.assertEqual(self.as_user(self.superuser).delete("/api/drafts/{}/".format(draft_id)).status_code, 405)
        self.assertDenied(self.as_anon().get("/api/drafts/{}/".format(draft_id)))

    def test_draft_owner_cannot_be_chosen_by_the_client(self):
        resp = self.as_user(self.outsider).post(
            "/api/drafts/", {"data": {"x": 1}, "owner": self.lab_a_admin.id}, format="json"
        )
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertNotIn("owner", resp.data)
        self.assertEqual(Draft.objects.get(pk=resp.data["id"]).owner, self.outsider)


class MassAssignmentTests(ApiTestCase):
    """Fields the lab sets through its own actions are ignored when sent by others."""

    def test_named_submitter_cannot_set_lab_only_fields(self):
        from dnaorder.tests.base import make_submission, make_submission_type
        from dnaorder.tests.test_payment_required import submission_payload
        free = make_submission_type(self.lab_a, name="Free", payment_required=False)
        submission = make_submission(free)
        payload = submission_payload(
            free, locked=True, confirmed="2020-01-01T00:00:00Z", cancelled="2020-01-01T00:00:00Z",
            completed="2020-01-01T00:00:00Z", samples_received="2020-01-01", received_by=self.submitter.id,
            comments="edited",
        )
        resp = self.as_submitter().put("/api/submissions/{}/".format(submission.id), payload, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        submission.refresh_from_db()
        self.assertEqual(submission.comments, "edited")
        self.assertFalse(submission.locked)
        for field in ["confirmed", "cancelled", "completed", "samples_received", "received_by"]:
            self.assertIsNone(getattr(submission, field), field)

    def test_lab_member_can_still_set_them(self):
        from dnaorder.tests.base import make_submission, make_submission_type
        from dnaorder.tests.test_payment_required import submission_payload
        free = make_submission_type(self.lab_a, name="Free", payment_required=False)
        submission = make_submission(free)
        resp = self.as_user(self.lab_a_member).put(
            "/api/submissions/{}/".format(submission.id), submission_payload(free, locked=True), format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        submission.refresh_from_db()
        self.assertTrue(submission.locked)

    def test_users_are_not_listed_on_a_submission(self):
        resp = self.as_submitter().get("/api/submissions/{}/".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertNotIn("users", resp.data)
