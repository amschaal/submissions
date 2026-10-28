"""Submission files are downloaded through the API (nginx only serves logos from /media).

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_submission_files
"""
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from dnaorder.models import SubmissionFile
from dnaorder.tests.base import ApiTestCase

MEDIA_ROOT = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(MEDIA_ROOT, ignore_errors=True)


@override_settings(MEDIA_ROOT=MEDIA_ROOT, BASE_URI='https://coreomics.example')
class SubmissionFileDownloadTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.submission_file = SubmissionFile.objects.create(submission=self.sub_a, file=SimpleUploadedFile('results.csv', b'a,b\n1,2\n'))

    def test_file_reads_back_as_the_download_url(self):
        resp = self.as_anon().get(f'/api/submission_files/?submission={self.sub_a.id}')
        self.assertEqual(resp.status_code, 200, resp.content)
        rows = resp.data['results'] if isinstance(resp.data, dict) else resp.data
        url = rows[0]['file']
        self.assertTrue(url.startswith('https://coreomics.example/'), url)
        self.assertTrue(url.endswith(f'/api/submission_files/{self.submission_file.id}/download/'), url)
        self.assertNotIn('/media/', url)

    def test_download_by_file_id(self):
        resp = self.as_anon().get(f'/api/submission_files/{self.submission_file.id}/download/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b''.join(resp.streaming_content), b'a,b\n1,2\n')
        self.assertIn('attachment; filename="results.csv"', resp['Content-Disposition'])

    def test_unknown_or_missing_file_is_404(self):
        self.assertEqual(self.as_anon().get('/api/submission_files/000000000000/download/').status_code, 404)
        self.submission_file.file.storage.delete(self.submission_file.file.name)
        self.assertEqual(self.as_anon().get(f'/api/submission_files/{self.submission_file.id}/download/').status_code, 404)

    def test_listing_still_requires_a_submission_id(self):
        self.assertDenied(self.as_anon().get('/api/submission_files/'))
