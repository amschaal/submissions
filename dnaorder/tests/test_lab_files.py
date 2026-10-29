"""Lab files: public vs internal visibility, lab member management, and storage outside MEDIA_ROOT.

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_lab_files
"""
import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from dnaorder.tests.base import ApiTestCase
from dnaorder.models import LabFile
from dnaorder.storage import protected_storage

PROTECTED_ROOT = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(PROTECTED_ROOT, ignore_errors=True)


def upload(name='template.xlsx', content=b'template contents'):
    return SimpleUploadedFile(name, content)


@override_settings(PROTECTED_MEDIA_ROOT=PROTECTED_ROOT)
class LabFileFixture(ApiTestCase):
    def make_file(self, internal=False, lab=None, **fields):
        return LabFile.objects.create(**{'lab': lab or self.lab_a, 'name': 'Template', 'internal': internal, 'file': upload(), **fields})

    def download(self, lab_file, client):
        resp = client.get(f'/api/lab_files/{lab_file.pk}/download/')
        if resp.status_code == 200:
            # Consuming streaming_content closes the response; calling resp.close() directly would
            # fire request_finished outside the test client and close the test DB connection.
            resp.content_bytes = b''.join(resp.streaming_content)
        return resp

    def listed_ids(self, client, query=''):
        resp = client.get('/api/lab_files/' + query)
        self.assertEqual(resp.status_code, 200, resp.content)
        return {item['id'] for item in resp.data}


class LabFileVisibilityTests(LabFileFixture):
    def test_public_file_is_fetchable_by_anyone_but_only_listed_for_lab_staff(self):
        lab_file = self.make_file()
        for client in [self.as_anon(), self.as_user(self.outsider), self.as_user(self.lab_b_member)]:
            self.assertNotIn(str(lab_file.pk), self.listed_ids(client))
            self.assertEqual(client.get(f'/api/lab_files/{lab_file.pk}/').status_code, 200)
        self.assertIn(str(lab_file.pk), self.listed_ids(self.as_user(self.lab_a_associate)))
        resp = self.download(lab_file, self.as_anon())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_bytes, b'template contents')
        self.assertIn('attachment; filename="template.xlsx"', resp['Content-Disposition'])

    def test_internal_file_is_hidden_from_users_without_a_lab_permission(self):
        lab_file = self.make_file(internal=True)
        for client in [self.as_anon(), self.as_user(self.outsider), self.as_user(self.lab_b_member)]:
            self.assertNotIn(str(lab_file.pk), self.listed_ids(client))
            self.assertEqual(self.download(lab_file, client).status_code, 404)
            self.assertEqual(client.get(f'/api/lab_files/{lab_file.pk}/').status_code, 404)

    def test_internal_file_is_downloadable_with_any_lab_permission(self):
        lab_file = self.make_file(internal=True)
        for user in [self.lab_a_admin, self.lab_a_member, self.lab_a_associate, self.inst_admin, self.superuser]:
            client = self.as_user(user)
            self.assertIn(str(lab_file.pk), self.listed_ids(client), user.username)
            resp = self.download(lab_file, client)
            self.assertEqual(resp.status_code, 200, user.username)
            self.assertEqual(resp['Cache-Control'], 'private, no-store')

    def test_lab_and_internal_filters(self):
        public_a, internal_a, public_b = self.make_file(), self.make_file(internal=True), self.make_file(lab=self.lab_b)
        client = self.as_user(self.superuser)
        self.assertEqual(self.listed_ids(client, '?lab=lab-a'), {str(public_a.pk), str(internal_a.pk)})
        self.assertEqual(self.listed_ids(client, '?lab=lab-a&internal=false'), {str(public_a.pk)})
        self.assertIn(str(public_b.pk), self.listed_ids(client, '?lab=lab-b'))

    def test_stored_outside_media_root_and_path_not_exposed(self):
        lab_file = self.make_file()
        self.assertTrue(protected_storage.path(lab_file.file.name).startswith(PROTECTED_ROOT))
        data = self.as_anon().get(f'/api/lab_files/{lab_file.pk}/').data
        self.assertNotIn('file', data)
        self.assertEqual(data['filename'], 'template.xlsx')
        self.assertTrue(data['url'].endswith(f'/api/lab_files/{lab_file.pk}/download/'))

    def test_bad_id_is_404(self):
        self.assertEqual(self.as_anon().get('/api/lab_files/not-a-uuid/download/').status_code, 404)


class LabFileManagementTests(LabFileFixture):
    def create(self, user, **data):
        payload = {'lab': self.lab_a.id, 'name': 'Plate layout', 'internal': True, 'file': upload(), **data}
        return self.as_user(user).post('/api/lab_files/', payload, format='multipart')

    def test_lab_members_can_upload(self):
        for user in [self.lab_a_admin, self.lab_a_member, self.superuser]:
            resp = self.create(user)
            self.assertEqual(resp.status_code, 201, resp.content)
            lab_file = LabFile.objects.get(pk=resp.data['id'])
            self.assertEqual(lab_file.uploaded_by, user)
            self.assertTrue(lab_file.internal)

    def test_others_cannot_upload(self):
        self.assertDenied(self.as_anon().post('/api/lab_files/', {'lab': self.lab_a.id, 'name': 'x', 'file': upload()}, format='multipart'))
        for user in [self.lab_a_associate, self.lab_b_member, self.outsider]:
            self.assertDenied(self.create(user), user.username)
        self.assertFalse(LabFile.objects.exists())

    def test_others_cannot_modify_or_delete_a_public_file(self):
        lab_file = self.make_file()
        for user in [self.lab_a_associate, self.lab_b_member, self.outsider]:
            client = self.as_user(user)
            self.assertDenied(client.patch(f'/api/lab_files/{lab_file.pk}/', {'internal': True}, format='json'), user.username)
            self.assertDenied(client.delete(f'/api/lab_files/{lab_file.pk}/'), user.username)
        lab_file.refresh_from_db()
        self.assertFalse(lab_file.internal)

    def test_upload_size_limit(self):
        with override_settings(LAB_FILE_MAX_UPLOAD_MB=0):
            resp = self.create(self.lab_a_member)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('file', resp.data)

    def test_replacing_the_file_deletes_the_old_one_and_lab_is_fixed(self):
        lab_file = self.make_file()
        old_name = lab_file.file.name
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.as_user(self.lab_a_member).patch(
                f'/api/lab_files/{lab_file.pk}/', {'file': upload('v2.csv', b'new'), 'lab': self.lab_b.id}, format='multipart')
        self.assertEqual(resp.status_code, 200, resp.content)
        lab_file.refresh_from_db()
        self.assertEqual(lab_file.filename, 'v2.csv')
        self.assertEqual(lab_file.lab, self.lab_a)
        self.assertFalse(protected_storage.exists(old_name))
        self.assertTrue(protected_storage.exists(lab_file.file.name))

    def test_deleting_removes_the_stored_file(self):
        lab_file = self.make_file()
        path = protected_storage.path(lab_file.file.name)
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.as_user(self.lab_a_admin).delete(f'/api/lab_files/{lab_file.pk}/')
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(os.path.exists(path))
