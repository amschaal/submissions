"""Form file fields: upload first, attach when the submission is saved, templates from lab files.

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_file_fields
"""
import shutil
import tempfile
from datetime import timedelta
from io import StringIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings

from dnaorder.file_fields import PENDING_HOURS
from dnaorder.models import LabFile, Submission, SubmissionFile
from dnaorder.tests.base import ApiTestCase, make_submission_type
from dnaorder.tests.test_payment_required import submission_payload
from schema.utils import schema_to_filters

MEDIA_ROOT = tempfile.mkdtemp()
PROTECTED_ROOT = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
    shutil.rmtree(PROTECTED_ROOT, ignore_errors=True)


def file_schema(**plate):
    return {
        'properties': {'plate': {'type': 'string', 'format': 'file', 'title': 'Plate layout', 'accept': '.csv,.xlsx', **plate}, 'notes': {'type': 'string'}},
        'order': ['plate', 'notes'], 'required': [], 'layout': {},
    }


@override_settings(MEDIA_ROOT=MEDIA_ROOT, PROTECTED_MEDIA_ROOT=PROTECTED_ROOT)
class FileFieldFixture(ApiTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.type_files = make_submission_type(cls.lab_a, name='Lab A Files', payment_required=False, submission_schema=file_schema())

    def upload(self, client=None, name='plate.csv', content=b'a,b\n', **data):
        payload = {'type': self.type_files.id, 'variable': 'plate', 'file': SimpleUploadedFile(name, content), **data}
        return (client or self.as_anon()).post('/api/submission_files/field_upload/', payload, format='multipart')

    def upload_id(self, **kwargs):
        resp = self.upload(**kwargs)
        self.assertEqual(resp.status_code, 201, resp.content)
        return resp.data['id']

    def submit(self, **submission_data):
        return self.as_anon().post('/api/submissions/', submission_payload(self.type_files, submission_data=submission_data), format='json')

    def submitted(self, **submission_data):
        resp = self.submit(**submission_data)
        self.assertEqual(resp.status_code, 201, resp.content)
        return Submission.objects.get(id=resp.data['id'])

    def edit(self, submission, **submission_data):
        payload = submission_payload(self.type_files, submission_data=submission_data)
        return self.as_user(self.lab_a_admin).put(f'/api/submissions/{submission.id}/', payload, format='json')


class FieldUploadTests(FileFieldFixture):
    def test_upload_is_unattached_and_not_downloadable_yet(self):
        resp = self.upload()
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertIsNone(resp.data['file'])
        self.assertEqual(resp.data['variable'], 'plate')
        upload = SubmissionFile.objects.get(id=resp.data['id'])
        self.assertIsNone(upload.submission)
        self.assertEqual(self.as_anon().get(f'/api/submission_files/{upload.id}/download/').status_code, 404)
        self.assertEqual(self.as_anon().get(f'/api/submission_files/{upload.id}/').data['filename'], 'plate.csv')

    def test_rejected_uploads(self):
        cases = [
            ({'name': 'plate.exe'}, 'file'),
            ({'variable': 'notes'}, 'variable'),
            ({'variable': 'missing'}, 'variable'),
            ({'type': ''}, 'type'),
        ]
        for kwargs, field in cases:
            resp = self.upload(**kwargs)
            self.assertEqual(resp.status_code, 400, kwargs)
            self.assertIn(field, resp.data, kwargs)
        self.assertFalse(SubmissionFile.objects.exists())

    def test_size_limit(self):
        self.type_files.submission_schema = file_schema(max_size_mb=0.000001)
        self.type_files.save()
        self.assertEqual(self.upload().status_code, 400)

    def test_internal_type_needs_a_lab_member(self):
        internal = make_submission_type(self.lab_a, name='Internal', internal=True, payment_required=False, submission_schema=file_schema())
        self.assertEqual(self.upload(type=internal.id).status_code, 403)
        self.assertEqual(self.upload(client=self.as_user(self.lab_a_member), type=internal.id).status_code, 201)

    def test_upload_for_a_locked_submission_is_refused(self):
        submission = self.submitted()
        Submission.objects.filter(id=submission.id).update(locked=True)
        self.assertEqual(self.upload(submission=submission.id, type='').status_code, 403)


class AttachOnSaveTests(FileFieldFixture):
    def test_submitting_attaches_the_upload(self):
        file_id = self.upload_id()
        submission = self.submitted(plate=file_id)
        upload = SubmissionFile.objects.get(id=file_id)
        self.assertEqual(upload.submission, submission)
        self.assertEqual(submission.submission_data['plate'], file_id)
        listed = self.as_anon().get(f'/api/submission_files/?submission={submission.id}').data['results']
        self.assertEqual([(f['id'], f['variable']) for f in listed], [(file_id, 'plate')])
        resp = self.as_anon().get(f'/api/submission_files/{file_id}/download/')
        self.assertEqual(b''.join(resp.streaming_content), b'a,b\n')

    def test_unknown_used_or_expired_uploads_are_rejected(self):
        used = self.upload_id()
        self.submitted(plate=used)
        expired = self.upload_id()
        SubmissionFile.objects.filter(id=expired).update(uploaded_at=SubmissionFile.objects.get(id=expired).uploaded_at - timedelta(hours=PENDING_HOURS + 1))
        other_field = SubmissionFile.objects.create(variable='other', file=SimpleUploadedFile('x.csv', b'x'))
        for file_id in ['nope', used, expired, other_field.id]:
            resp = self.submit(plate=file_id)
            self.assertEqual(resp.status_code, 400, file_id)
            self.assertIn('plate', resp.data['submission_data'], file_id)

    def test_upload_checked_against_the_field_it_is_used_for(self):
        # Uploaded for another type's field with the same name, but this field only accepts .csv.
        other = make_submission_type(self.lab_a, name='Any file', payment_required=False, submission_schema=file_schema(accept=''))
        file_id = self.upload_id(type=other.id, name='plate.txt')
        resp = self.submit(plate=file_id)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('plate', resp.data['submission_data'])

    def test_editing_keeps_or_replaces_the_file(self):
        first = self.upload_id()
        submission = self.submitted(plate=first)
        self.assertEqual(self.edit(submission, plate=first, notes='kept').status_code, 200)
        second = self.upload_id(submission=submission.id, type='')
        resp = self.edit(submission, plate=second)
        self.assertEqual(resp.status_code, 200, resp.content)
        submission.refresh_from_db()
        self.assertEqual(submission.submission_data['plate'], second)
        # The replaced file stays attached, e.g. for older versions of the submission.
        self.assertEqual(set(submission.files.values_list('id', flat=True)), {first, second})

    def test_form_uploads_cannot_be_deleted_or_changed_directly(self):
        file_id = self.upload_id()
        submission = self.submitted(plate=file_id)
        url = f'/api/submission_files/{file_id}/?submission={submission.id}'
        self.assertEqual(self.as_user(self.lab_a_admin).delete(url).status_code, 403)
        resp = self.as_user(self.lab_a_admin).patch(url, {'file': SimpleUploadedFile('new.csv', b'n')}, format='multipart')
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(SubmissionFile.objects.filter(id=file_id).exists())

    def test_attachments_still_need_a_submission(self):
        resp = self.as_anon().post('/api/submission_files/', {'file': SimpleUploadedFile('a.txt', b'a')}, format='multipart')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('submission', resp.data)

    def test_cleanup_deletes_only_old_unattached_uploads(self):
        attached = self.upload_id()
        self.submitted(plate=attached)
        fresh, stale = self.upload_id(), self.upload_id()
        old = SubmissionFile.objects.get(id=stale)
        SubmissionFile.objects.filter(id__in=[stale, attached]).update(uploaded_at=old.uploaded_at - timedelta(hours=PENDING_HOURS + 1))
        call_command('cleanup_uploads', stdout=StringIO())
        self.assertEqual(set(SubmissionFile.objects.values_list('id', flat=True)), {attached, fresh})
        self.assertFalse(old.file.storage.exists(old.file.name))

    def test_file_fields_are_not_search_filters(self):
        self.assertEqual(list(schema_to_filters(file_schema())), ['notes'])


class TemplateTests(FileFieldFixture):
    def save_schema(self, lab_file, lab=None):
        payload = {'submission_schema': file_schema(template=str(lab_file.pk) if lab_file else 'not-a-uuid')}
        return self.as_user(self.lab_a_admin).patch(f'/api/submission_types/{self.type_files.id}/', payload, format='json')

    def lab_file(self, lab=None, internal=False):
        return LabFile.objects.create(lab=lab or self.lab_a, name='Template', internal=internal, file=SimpleUploadedFile('t.xlsx', b't'))

    def test_public_template_of_the_lab_is_allowed(self):
        self.assertEqual(self.save_schema(self.lab_file()).status_code, 200)

    def test_internal_foreign_or_unknown_templates_are_rejected(self):
        for lab_file in [self.lab_file(internal=True), self.lab_file(lab=self.lab_b), None]:
            resp = self.save_schema(lab_file)
            self.assertEqual(resp.status_code, 400, lab_file)
            self.assertIn('submission_schema', resp.data)
