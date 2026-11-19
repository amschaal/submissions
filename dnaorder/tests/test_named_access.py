"""What signed-in users without lab permissions can do with a submission.

They can only open the submissions that name them (submitter, PI or contact
email).  Until a submission is locked they can edit it, cancel it and add
files and notes; they can never delete it or see the lab's private notes.
To everyone else the submission does not exist (404), whether or not they
know its id.

Fixture users (see ``ApiTestCase``): ``submitter`` and ``pi_user`` are named
on every fixture submission, ``contact_user`` on ``sub_a`` only, ``outsider``
on none.
"""
import shutil
import tempfile

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient

from dnaorder.models import Contact, Draft, Note, Submission, SubmissionFile
from dnaorder.tests.base import (
    ApiTestCase, make_note, make_submission, make_submission_type,
)
from dnaorder.tests.test_payment_required import submission_payload

MEDIA_ROOT = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(MEDIA_ROOT, ignore_errors=True)


def rows(response):
    return response.data["results"] if isinstance(response.data, dict) else response.data


class NamedAccessFixture(ApiTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # No payment needed, so a plain payload is a valid create/edit.
        cls.type_free = make_submission_type(cls.lab_a, name="Lab A Free", payment_required=False)
        cls.sub_free = make_submission(cls.type_free, first_name="Free")

    @staticmethod
    def url(submission, suffix=""):
        return "/api/submissions/{}/{}".format(submission.id, suffix)

    def put(self, user, submission=None, **overrides):
        submission = submission or self.sub_free
        return self.as_user(user).put(self.url(submission), submission_payload(submission.type, **overrides), format="json")


class ViewTests(NamedAccessFixture):
    def test_named_people_can_open_their_submission(self):
        for user in [self.submitter, self.pi_user, self.contact_user]:
            resp = self.as_user(user).get(self.url(self.sub_a))
            self.assertEqual(resp.status_code, 200, user.username)
            self.assertEqual(resp.data["id"], self.sub_a.id)

    def test_named_on_one_submission_is_not_named_on_another(self):
        self.assertNotFound(self.as_user(self.contact_user).get(self.url(self.sub_b)))
        self.assertNotFound(self.as_user(self.contact_user).get(self.url(self.sub_a_locked)))

    def test_knowing_the_id_is_not_enough(self):
        for submission in [self.sub_a, self.sub_a_locked, self.sub_b]:
            self.assertNotFound(self.as_user(self.outsider).get(self.url(submission)))

    def test_hidden_submission_looks_like_a_missing_one(self):
        hidden = self.as_user(self.outsider).get(self.url(self.sub_a))
        missing = self.as_user(self.outsider).get("/api/submissions/000000000000/")
        self.assertEqual((hidden.status_code, hidden.data), (missing.status_code, missing.data))

    def test_staff_reach_their_own_labs_and_institution(self):
        for user in [self.lab_a_admin, self.lab_a_member, self.lab_a_associate, self.inst_admin, self.superuser]:
            self.assertEqual(self.as_user(user).get(self.url(self.sub_a)).status_code, 200, user.username)
        self.assertEqual(self.as_user(self.lab_b_member).get(self.url(self.sub_b)).status_code, 200)
        self.assertNotFound(self.as_user(self.lab_b_member).get(self.url(self.sub_a)))

    def test_my_submissions_lists_what_names_the_user(self):
        mine = {row["id"] for row in rows(self.as_user(self.contact_user).get("/api/submissions/"))}
        self.assertEqual(mine, {self.sub_a.id})
        mine = {row["id"] for row in rows(self.as_user(self.contact_user).get("/api/submissions/?my_submissions"))}
        self.assertEqual(mine, {self.sub_a.id})
        self.assertEqual(rows(self.as_user(self.outsider).get("/api/submissions/")), [])

    def test_download_follows_the_same_rule(self):
        path = self.url(self.sub_a, "download/?data=submission&export_format=csv")
        for user in [self.submitter, self.contact_user, self.lab_a_associate]:
            resp = self.as_user(user).get(path)
            self.assertEqual(resp.status_code, 200, user.username)
            self.assertIn("attachment", resp.get("Content-Disposition", ""))
        for user in [self.outsider, self.lab_b_member]:
            self.assertNotFound(self.as_user(user).get(path))


class EditTests(NamedAccessFixture):
    def test_named_people_can_edit_until_locked(self):
        for user in [self.submitter, self.pi_user]:
            resp = self.put(user, comments="by " + user.username)
            self.assertEqual(resp.status_code, 200, resp.content)
        self.sub_free.refresh_from_db()
        self.assertEqual(self.sub_free.comments, "by pi_user")
        Submission.objects.filter(pk=self.sub_free.pk).update(locked=True)
        self.assertEqual(self.put(self.submitter, comments="late").status_code, 403)

    def test_others_cannot_edit(self):
        for user in [self.outsider, self.contact_user, self.lab_b_member]:
            self.assertNotFound(self.put(user, comments="hijacked"))
        self.sub_free.refresh_from_db()
        self.assertIsNone(self.sub_free.comments)

    def test_adding_a_contact_shares_the_submission(self):
        contact = {"first_name": "Out", "last_name": "Sider", "email": "Out@Example.com"}
        self.assertNotFound(self.as_user(self.outsider).get(self.url(self.sub_free)))
        self.assertEqual(self.put(self.submitter, contacts=[contact]).status_code, 200)
        self.assertEqual(self.as_user(self.outsider).get(self.url(self.sub_free)).status_code, 200)
        self.assertEqual(self.put(self.outsider, contacts=[contact], comments="shared").status_code, 200)
        # ...and removing them takes it away again.
        self.assertEqual(self.put(self.submitter, contacts=[]).status_code, 200)
        self.assertNotFound(self.as_user(self.outsider).get(self.url(self.sub_free)))

    def test_cannot_remove_yourself(self):
        resp = self.put(self.submitter, email="someone.else@example.com")
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("email", resp.data)
        self.sub_free.refresh_from_db()
        self.assertEqual(self.sub_free.email, "submitter@example.com")
        # Staying on as a contact is fine.
        me = {"first_name": "Sub", "last_name": "Mitter", "email": "submitter@example.com"}
        resp = self.put(self.submitter, email="someone.else@example.com", contacts=[me])
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_lab_staff_can_change_who_is_named(self):
        resp = self.put(self.lab_a_member, email="replacement@example.com", pi_email="newpi@example.com")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertNotFound(self.as_user(self.submitter).get(self.url(self.sub_free)))


class CreateTests(NamedAccessFixture):
    def create(self, user, **overrides):
        return self.as_user(user).post("/api/submissions/", submission_payload(self.type_free, **overrides), format="json")

    def test_user_must_name_themselves(self):
        before = Submission.objects.count()
        resp = self.create(self.outsider)  # names submitter@ and pi@ only
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("email", resp.data)
        self.assertEqual(Submission.objects.count(), before)

    def test_submitter_pi_or_contact_can_create(self):
        me = {"first_name": "Out", "last_name": "Sider", "email": self.outsider.email}
        for overrides in [{"email": self.outsider.email}, {"pi_email": self.outsider.email.upper()}, {"contacts": [me]}]:
            resp = self.create(self.outsider, **overrides)
            self.assertEqual(resp.status_code, 201, resp.content)
            self.assertEqual(self.as_user(self.outsider).get("/api/submissions/{}/".format(resp.data["id"])).status_code, 200)

    def test_creating_sends_the_confirmation_email(self):
        mail.outbox.clear()
        self.assertEqual(self.create(self.submitter).status_code, 201)
        confirmations = [message for message in mail.outbox if "submitter@example.com" in message.to]
        self.assertEqual(len(confirmations), 1)
        self.assertIn("You will be asked to sign in", confirmations[0].body)

    def test_lab_staff_can_create_for_someone_else(self):
        self.assertEqual(self.create(self.lab_a_member).status_code, 201)
        self.assertEqual(self.create(self.lab_a_associate).status_code, 201)

    def test_staff_of_another_lab_are_treated_like_any_user(self):
        self.assertEqual(self.create(self.lab_b_member).status_code, 400)


class CancelConfirmDeleteTests(NamedAccessFixture):
    def test_named_user_can_cancel_until_locked(self):
        resp = self.as_submitter().post(self.url(self.sub_free, "cancel/"), {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIsNotNone(Submission.objects.get(pk=self.sub_free.pk).cancelled)
        resp = self.as_submitter().post(self.url(self.sub_a_locked, "cancel/"), {}, format="json")
        self.assertEqual(resp.status_code, 403, resp.content)
        self.assertIsNone(Submission.objects.get(pk=self.sub_a_locked.pk).cancelled)

    def test_others_cannot_cancel_or_confirm(self):
        for action in ["cancel/", "confirm/"]:
            self.assertNotFound(self.as_user(self.outsider).post(self.url(self.sub_free, action), {}, format="json"))
        submission = Submission.objects.get(pk=self.sub_free.pk)
        self.assertIsNone(submission.cancelled)
        self.assertIsNone(submission.confirmed)

    def test_lab_member_can_cancel_a_locked_submission(self):
        resp = self.as_user(self.lab_a_member).post(self.url(self.sub_a_locked, "cancel/"), {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_named_user_can_confirm(self):
        resp = self.as_user(self.contact_user).post(self.url(self.sub_a, "confirm/"), {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIsNotNone(Submission.objects.get(pk=self.sub_a.pk).confirmed)

    def test_only_lab_admins_delete(self):
        for user in [self.submitter, self.pi_user, self.lab_a_member, self.lab_a_associate, self.inst_admin]:
            self.assertEqual(self.as_user(user).delete(self.url(self.sub_free)).status_code, 403, user.username)
        self.assertNotFound(self.as_user(self.outsider).delete(self.url(self.sub_free)))
        self.assertTrue(Submission.objects.filter(pk=self.sub_free.pk).exists())
        self.assertIn(self.as_user(self.lab_a_admin).delete(self.url(self.sub_free)).status_code, (200, 204))
        self.assertFalse(Submission.objects.filter(pk=self.sub_free.pk).exists())


class InternalTypeTests(NamedAccessFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.type_internal = make_submission_type(cls.lab_a, name="Internal", internal=True, payment_required=False)
        cls.sub_internal = make_submission(cls.type_internal, first_name="Internal")

    def test_named_people_can_only_view(self):
        self.assertEqual(self.as_submitter().get(self.url(self.sub_internal)).status_code, 200)
        self.assertEqual(self.put(self.submitter, self.sub_internal, comments="x").status_code, 403)
        self.assertEqual(self.as_submitter().post(self.url(self.sub_internal, "cancel/"), {}, format="json").status_code, 403)
        submission = Submission.objects.get(pk=self.sub_internal.pk)
        self.assertIsNone(submission.comments)
        self.assertIsNone(submission.cancelled)

    def test_lab_member_can_edit(self):
        self.assertEqual(self.put(self.lab_a_member, self.sub_internal, comments="x").status_code, 200)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FileTests(NamedAccessFixture):
    def setUp(self):
        super().setUp()
        self.file = SubmissionFile.objects.create(submission=self.sub_a, file=SimpleUploadedFile("results.csv", b"a,b\n"))

    def attach(self, user, submission):
        payload = {"submission": submission.id, "file": SimpleUploadedFile("extra.txt", b"x")}
        return self.as_user(user).post("/api/submission_files/", payload, format="multipart")

    def test_named_people_and_lab_staff_can_list_and_download(self):
        for user in [self.submitter, self.contact_user, self.lab_a_associate]:
            client = self.as_user(user)
            listing = client.get("/api/submission_files/?submission={}".format(self.sub_a.id))
            self.assertEqual([row["id"] for row in rows(listing)], [self.file.id], user.username)
            self.assertEqual(client.get("/api/submission_files/{}/download/".format(self.file.id)).status_code, 200)

    def test_others_cannot_list_look_up_or_download(self):
        for user in [self.outsider, self.lab_b_member]:
            client = self.as_user(user)
            self.assertNotFound(client.get("/api/submission_files/?submission={}".format(self.sub_a.id)))
            self.assertNotFound(client.get("/api/submission_files/{}/".format(self.file.id)))
            self.assertNotFound(client.get("/api/submission_files/{}/download/".format(self.file.id)))

    def test_named_user_can_attach_a_file_and_is_recorded_as_uploader(self):
        resp = self.attach(self.contact_user, self.sub_a)
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(SubmissionFile.objects.get(pk=resp.data["id"]).uploaded_by, self.contact_user)

    def test_others_cannot_attach_files(self):
        before = SubmissionFile.objects.count()
        self.assertNotFound(self.attach(self.outsider, self.sub_a))
        self.assertNotFound(self.attach(self.contact_user, self.sub_b))
        self.assertEqual(SubmissionFile.objects.count(), before)

    def test_file_stays_on_its_submission(self):
        file_id = self.attach(self.contact_user, self.sub_a).data["id"]
        url = "/api/submission_files/{}/".format(file_id)
        for target in [self.sub_b, self.sub_a_locked]:
            resp = self.as_user(self.contact_user).patch(url, {"submission": target.id}, format="json")
            self.assertEqual(resp.status_code, 400, resp.content)
            self.assertIn("submission", resp.data)
        # Lab staff can't move one between their own submissions either.
        resp = self.as_user(self.lab_a_admin).patch(url, {"submission": self.sub_a_locked.id}, format="json")
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertEqual(SubmissionFile.objects.get(pk=file_id).submission_id, self.sub_a.id)
        # Sending the submission it already has is not a move.
        resp = self.as_user(self.contact_user).patch(url, {"submission": self.sub_a.id}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_only_staff_delete_files_of_a_locked_submission(self):
        locked_file = SubmissionFile.objects.create(submission=self.sub_a_locked, file=SimpleUploadedFile("l.csv", b"l"))
        url = "/api/submission_files/{}/".format(locked_file.id)
        self.assertEqual(self.as_submitter().delete(url).status_code, 403)
        self.assertNotFound(self.as_user(self.outsider).delete(url))
        self.assertTrue(SubmissionFile.objects.filter(pk=locked_file.pk).exists())


class NoteTests(NamedAccessFixture):
    def setUp(self):
        super().setUp()
        self.public = make_note(self.sub_a, "public", public=True)
        self.private = make_note(self.sub_a, "private", public=False)

    def texts(self, user, submission=None):
        resp = self.as_user(user).get("/api/notes/?submission={}".format((submission or self.sub_a).id))
        self.assertEqual(resp.status_code, 200, resp.content)
        return {note["text"] for note in rows(resp)}

    def post(self, user, **data):
        payload = {"submission": self.sub_a.id, "text": "hello", "type": Note.TYPE_NOTE, **data}
        return self.as_user(user).post("/api/notes/", payload, format="json")

    def test_named_people_see_public_notes_only(self):
        for user in [self.submitter, self.contact_user, self.lab_a_associate]:
            self.assertEqual(self.texts(user), {"public"}, user.username)
        self.assertEqual(self.texts(self.lab_a_member), {"public", "private"})

    def test_others_cannot_read_or_write_notes(self):
        for user in [self.outsider, self.lab_b_member]:
            self.assertNotFound(self.as_user(user).get("/api/notes/?submission={}".format(self.sub_a.id)))
            self.assertNotFound(self.post(user))
        self.assertEqual(Note.objects.filter(submission=self.sub_a).count(), 2)

    def test_note_for_an_unknown_submission_is_404(self):
        self.assertNotFound(self.post(self.submitter, submission="000000000000"))
        self.assertNotFound(self.as_submitter().post("/api/notes/", {"text": "no submission"}, format="json"))

    def test_named_user_writes_public_notes_under_their_own_name(self):
        resp = self.post(self.contact_user, public=False, type=Note.TYPE_LOG, text="from a contact")
        self.assertEqual(resp.status_code, 201, resp.content)
        note = Note.objects.get(pk=resp.data["id"])
        self.assertTrue(note.public)
        self.assertEqual(note.type, Note.TYPE_NOTE)
        self.assertEqual(note.created_by, self.contact_user)
        self.assertIn("from a contact", self.texts(self.submitter))

    def test_lab_member_can_write_a_private_note(self):
        resp = self.post(self.lab_a_member, public=False, text="lab only")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertFalse(Note.objects.get(pk=resp.data["id"]).public)
        self.assertNotIn("lab only", self.texts(self.submitter))

    def test_reply_must_belong_to_the_same_submission(self):
        elsewhere = make_note(self.sub_b, "elsewhere", public=True)
        resp = self.post(self.submitter, parent=elsewhere.id)
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("parent", resp.data)
        self.assertEqual(self.post(self.submitter, parent=self.public.id).status_code, 201)

    def test_author_can_edit_their_note(self):
        note_id = self.post(self.contact_user, text="first draft").data["id"]
        url = "/api/notes/{}/?submission={}".format(note_id, self.sub_a.id)
        resp = self.as_user(self.contact_user).patch(url, {"text": "second draft"}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        note = Note.objects.get(pk=note_id)
        self.assertEqual((note.text, note.submission_id), ("second draft", self.sub_a.id))
        self.assertDenied(self.as_submitter().patch(url, {"text": "not mine"}, format="json"))

    def test_note_stays_on_its_submission(self):
        note_id = self.post(self.contact_user, text="mine").data["id"]
        url = "/api/notes/{}/?submission={}".format(note_id, self.sub_a.id)
        for method in ("patch", "put"):
            body = {"submission": self.sub_b.id, "text": "moved", "type": Note.TYPE_NOTE, "send_email": True}
            resp = getattr(self.as_user(self.contact_user), method)(url, body, format="json")
            self.assertEqual(resp.status_code, 400, resp.content)
            self.assertIn("submission", resp.data)
            self.assertNotIn("emails", resp.data)
        note = Note.objects.get(pk=note_id)
        self.assertEqual((note.text, note.submission_id), ("mine", self.sub_a.id))
        self.assertFalse(Note.objects.filter(submission=self.sub_b).exists())


class DraftTests(NamedAccessFixture):
    def save(self, user, data):
        resp = self.as_user(user).post("/api/drafts/", {"data": data}, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        return "/api/drafts/{}/".format(resp.data["id"])

    def test_owner_can_reopen_and_resave(self):
        url = self.save(self.outsider, {"first_name": "Dra", "notes": 1})
        self.assertEqual(self.as_user(self.outsider).get(url).data["data"], {"first_name": "Dra", "notes": 1})
        resp = self.as_user(self.outsider).put(url, {"data": {"notes": 2}}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(Draft.objects.get(pk=resp.data["id"]).owner, self.outsider)

    def test_other_users_cannot_open_someone_elses_draft(self):
        url = self.save(self.outsider, {"email": "nobody@example.com"})
        for user in [self.submitter, self.pi_user]:
            self.assertNotFound(self.as_user(user).get(url))
            self.assertNotFound(self.as_user(user).put(url, {"data": {"x": 1}}, format="json"))

    def test_people_named_in_a_draft_can_open_it(self):
        contact = {"first_name": "Con", "last_name": "Tact", "email": "Contact@Example.com"}
        url = self.save(self.outsider, {"email": "nobody@example.com", "pi_email": "PI@example.com", "contacts": [contact]})
        for user in [self.pi_user, self.contact_user]:
            self.assertEqual(self.as_user(user).get(url).status_code, 200, user.username)
        self.assertNotFound(self.as_user(self.submitter).get(url))

    def test_draft_saved_before_sign_in_was_required_follows_who_it_names(self):
        draft = Draft.objects.create(data={"email": "submitter@example.com"})  # no owner
        url = "/api/drafts/{}/".format(draft.id)
        self.assertEqual(self.as_submitter().get(url).status_code, 200)
        self.assertNotFound(self.as_user(self.outsider).get(url))

    def test_staff_can_open_a_draft_to_help(self):
        url = self.save(self.outsider, {"email": "nobody@example.com"})
        self.assertEqual(self.as_user(self.lab_a_member).get(url).status_code, 200)


class CopyAndImportTests(NamedAccessFixture):
    def copy(self, user, submission):
        return self.as_user(user).get("/api/imports/get_submission/?url=/submissions/{}".format(submission.id))

    def test_copy_only_works_for_a_submission_the_user_can_open(self):
        resp = self.copy(self.contact_user, self.sub_a)
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["data"]["id"], self.sub_a.id)
        self.assertNotFound(self.copy(self.contact_user, self.sub_b))
        self.assertNotFound(self.copy(self.outsider, self.sub_a))
        self.assertNotFound(self.as_user(self.outsider).get("/api/imports/get_submission/?url=not-a-submission"))

    def test_import_records_are_for_staff(self):
        for user in [self.submitter, self.outsider]:
            self.assertDenied(self.as_user(user).get("/api/imports/"))
            self.assertDenied(self.as_user(user).post(
                "/api/imports/import_submission/", {"url": "/submissions/{}".format(self.sub_a.id)}, format="json"
            ))
        self.assertEqual(self.as_user(self.lab_a_member).get("/api/imports/").status_code, 200)

    def test_staff_cannot_import_a_submission_they_cannot_open(self):
        resp = self.as_user(self.lab_b_member).post(
            "/api/imports/import_submission/", {"url": "/submissions/{}".format(self.sub_a.id)}, format="json"
        )
        self.assertNotFound(resp)

    def test_schema_lookup_is_for_staff_and_follows_visibility(self):
        path = "/api/submission_types/get_submission_schema/?url=/submissions/{}".format(self.sub_a.id)
        self.assertDenied(self.as_submitter().get(path))
        self.assertEqual(self.as_user(self.lab_a_member).get(path).status_code, 200)
        self.assertNotFound(self.as_user(self.lab_b_member).get(path))


class StaffOnlyReferenceTests(NamedAccessFixture):
    def test_non_staff_cannot_use_staff_lookups(self):
        for path in ["/api/billing/services/", "/api/groups/", "/api/group_institutions/", "/api/users/"]:
            for user in [self.submitter, self.outsider]:
                self.assertDenied(self.as_user(user).get(path), path)
            self.assertEqual(self.as_user(self.lab_a_member).get(path).status_code, 200, path)

    def test_signed_in_users_can_load_what_the_form_needs(self):
        for path in ["/api/labs/", "/api/labs/lab-a/", "/api/submission_types/", "/api/validators/",
                     "/api/vocabularies/", "/api/plugins/", "/api/submission_types/{}/".format(self.type_free.id)]:
            self.assertEqual(self.as_user(self.outsider).get(path).status_code, 200, path)


class TokenClientTests(NamedAccessFixture):
    """API clients authenticate with a staff user's token; they follow the same rule."""

    def test_staff_token_reads_and_writes_its_labs_submissions(self):
        client = self.as_token(self.lab_a_member)
        self.assertEqual(client.get(self.url(self.sub_a)).status_code, 200)
        listed = {row["id"] for row in rows(client.get("/api/submissions/?lab=lab-a"))}
        self.assertIn(self.sub_a.id, listed)
        self.assertEqual(client.get(self.url(self.sub_a, "download/?data=submission&export_format=csv")).status_code, 200)
        self.assertEqual(client.get("/api/notes/?submission={}".format(self.sub_a.id)).status_code, 200)
        resp = client.put(self.url(self.sub_free), submission_payload(self.type_free, comments="via token"), format="json")
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_token_does_not_reach_other_labs(self):
        client = self.as_token(self.lab_b_member)
        self.assertNotFound(client.get(self.url(self.sub_a)))
        self.assertNotFound(client.get(self.url(self.sub_a, "download/?data=submission&export_format=csv")))

    def test_bad_token_is_refused(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token not-a-real-token")
        self.assertDenied(client.get(self.url(self.sub_a)))


class CsrfTests(NamedAccessFixture):
    def test_session_writes_need_the_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.submitter)
        self.assertEqual(client.get(self.url(self.sub_free)).status_code, 200)
        resp = client.put(self.url(self.sub_free), submission_payload(self.type_free, comments="x"), format="json")
        self.assertEqual(resp.status_code, 403, resp.content)
