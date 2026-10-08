"""Webhooks: lab-admin-only config, write-only encrypted secrets, SSRF guards, and dispatch on submission writes.

Run inside the api container:
    docker compose exec api python manage.py test webhooks
"""
from contextlib import contextmanager
from unittest import mock

import requests
from cryptography.fernet import Fernet
from django.test import override_settings
from rest_framework.authtoken.models import Token

from dnaorder.tests.base import ApiTestCase, make_submission, make_submission_type
from dnaorder.tests.test_payment_required import submission_payload
from webhooks.models import Webhook

PUBLIC_URL = 'https://8.8.8.8/hook'  # IP literals resolve without DNS
OTHER_URL = 'https://8.8.4.4/hook'
SECRET = 'Bearer s3cr3t-value'


@override_settings(WEBHOOK_ENCRYPTION_KEYS=[Fernet.generate_key().decode()], WEBHOOK_ASYNC=False, WEBHOOK_ALLOW_INSECURE=0)
class WebhookFixture(ApiTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.type_free = make_submission_type(cls.lab_a, name='Lab A Free Type', payment_required=False)
        cls.sub_free = make_submission(cls.type_free)

    def hook(self, **fields):
        return Webhook.objects.create(**{'lab': self.lab_a, 'url': PUBLIC_URL, 'secret': SECRET, **fields})

    def create(self, user=None, **data):
        payload = {'lab': self.lab_a.id, 'url': PUBLIC_URL, 'secret': SECRET, **data}
        return self.as_user(user or self.lab_a_admin).post('/api/webhooks/', payload, format='json')

    @contextmanager
    def capture_posts(self, status=200):
        """Mock outbound POSTs and run on-commit callbacks (where webhooks are sent) on exit."""
        with mock.patch('webhooks.delivery.requests.post') as post, self.captureOnCommitCallbacks(execute=True):
            post.return_value.__enter__.return_value.status_code = status
            yield post


class WebhookConfigTests(WebhookFixture):
    def test_secret_is_write_only_and_encrypted_at_rest(self):
        resp = self.create()
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertNotIn('secret', resp.data)
        self.assertTrue(resp.data['has_secret'])
        webhook = Webhook.objects.get(pk=resp.data['id'])
        self.assertNotIn('s3cr3t', webhook.encrypted_secret)
        self.assertEqual(webhook.secret, SECRET)
        for url in ['/api/webhooks/', f'/api/webhooks/{webhook.id}/', f'/api/labs/{self.lab_a.lab_id}/',
                    f'/api/submission_types/{self.type_free.id}/', f'/api/submissions/{self.sub_free.id}/']:
            self.assertNotIn('s3cr3t', self.as_user(self.lab_a_admin).get(url).content.decode(), url)

    def test_secret_is_kept_unless_replaced_or_cleared(self):
        webhook = self.hook()
        url = f'/api/webhooks/{webhook.id}/'
        self.as_user(self.lab_a_admin).patch(url, {'enabled': False}, format='json')
        webhook.refresh_from_db()
        self.assertEqual(webhook.secret, SECRET)
        self.as_user(self.lab_a_admin).patch(url, {'secret': ''}, format='json')
        webhook.refresh_from_db()
        self.assertEqual(webhook.encrypted_secret, '')

    def test_lab_admin_can_reveal_secret(self):
        webhook = self.hook()
        resp = self.as_user(self.lab_a_admin).post(f'/api/webhooks/{webhook.id}/reveal_secret/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['secret'], SECRET)
        self.assertEqual(resp['Cache-Control'], 'no-store')

    def test_reveal_requires_a_session_not_an_api_token(self):
        webhook = self.hook()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {Token.objects.create(user=self.lab_a_admin).key}')
        self.assertDenied(self.client.post(f'/api/webhooks/{webhook.id}/reveal_secret/'))

    def test_only_lab_admins_can_see_or_manage(self):
        webhook = self.hook()
        detail = f'/api/webhooks/{webhook.id}/'
        for user in [self.lab_a_member, self.lab_a_associate, self.lab_b_member, self.inst_admin, self.outsider]:
            client = self.as_user(user)
            self.assertEqual(client.get('/api/webhooks/').data, [], user)
            self.assertIn(client.get(detail).status_code, (403, 404), user)
            self.assertIn(client.post(detail + 'reveal_secret/').status_code, (403, 404), user)
            self.assertIn(client.patch(detail, {'url': OTHER_URL}, format='json').status_code, (403, 404), user)
            self.assertIn(client.delete(detail).status_code, (403, 404), user)
            self.assertDenied(self.create(user, submission_type=self.type_free.id))
        self.assertDenied(self.as_anon().get('/api/webhooks/'))
        webhook.refresh_from_db()
        self.assertEqual(webhook.url, PUBLIC_URL)

    def test_rejects_insecure_or_internal_urls(self):
        for url in ['http://8.8.8.8/', 'ftp://8.8.8.8/', 'https://127.0.0.1/', 'https://localhost/', 'https://[::1]/',
                    'https://169.254.169.254/latest/meta-data/', 'https://10.0.0.5/', 'https://user:pw@8.8.8.8/']:
            resp = self.create(url=url)
            self.assertEqual(resp.status_code, 400, url)
            self.assertIn('url', resp.data, url)

    def test_rejects_unsafe_auth_header_names(self):
        for name in ['', 'Host', 'content-length', 'X Bad', 'X-Bad:']:
            self.assertEqual(self.create(auth_header=name).status_code, 400, name)

    def test_secret_requires_an_encryption_key(self):
        with override_settings(WEBHOOK_ENCRYPTION_KEYS=[]):
            resp = self.create()
        self.assertEqual(resp.status_code, 400)
        self.assertIn('secret', resp.data)

    def test_url_is_required_unless_disabled(self):
        resp = self.create(url='')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('url', resp.data)
        override = self.create(url='', enabled=False, submission_type=self.type_free.id)  # switches webhooks off for this type
        self.assertEqual(override.status_code, 201, override.content)
        resp = self.as_user(self.lab_a_admin).patch(f"/api/webhooks/{override.data['id']}/", {'enabled': True}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('url', resp.data)

    def test_one_default_per_lab_and_one_override_per_type(self):
        self.hook()
        self.assertEqual(self.create().status_code, 400)
        self.assertEqual(self.create(submission_type=self.type_free.id).status_code, 201)
        self.assertEqual(self.create(submission_type=self.type_free.id).status_code, 400)
        self.assertEqual(self.create(submission_type=self.type_b.id).status_code, 400)  # another lab's type

    def test_lab_and_type_cannot_be_changed(self):
        webhook = self.hook()
        self.as_user(self.lab_a_admin).patch(f'/api/webhooks/{webhook.id}/', {'lab': self.lab_b.id, 'submission_type': self.type_b.id}, format='json')
        webhook.refresh_from_db()
        self.assertEqual((webhook.lab, webhook.submission_type), (self.lab_a, None))


class WebhookDeliveryTests(WebhookFixture):
    def test_create_and_update_send_a_thin_authenticated_event(self):
        self.hook()
        with self.capture_posts() as post:
            resp = self.as_anon().post('/api/submissions/', submission_payload(self.type_free), format='json')
        self.assertEqual(resp.status_code, 201, resp.content)
        post.assert_called_once()
        (url,), kwargs = post.call_args
        payload = kwargs['json']
        self.assertEqual(url, PUBLIC_URL)
        self.assertEqual(kwargs['headers']['Authorization'], SECRET)
        self.assertFalse(kwargs['allow_redirects'])
        self.assertEqual((payload['event'], payload['action'], payload['id'], payload['actor']), ('submission.created', 'create', resp.data['id'], None))
        self.assertTrue(payload['url'].endswith(f"api/submissions/{resp.data['id']}/"))
        self.assertNotIn('submission_data', payload)

        with self.capture_posts() as post:
            resp = self.as_user(self.lab_a_admin).put(f"/api/submissions/{resp.data['id']}/", submission_payload(self.type_free), format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        payload = post.call_args.kwargs['json']
        self.assertEqual((payload['event'], payload['action'], payload['actor']), ('submission.updated', 'update', 'lab_a_admin'))

    def test_status_actions_notify(self):
        self.hook()
        with self.capture_posts() as post:
            self.as_user(self.lab_a_admin).post(f'/api/submissions/{self.sub_free.id}/update_status/', {'status': 'Received'}, format='json')
            self.as_user(self.lab_a_admin).post(f'/api/submissions/{self.sub_free.id}/lock/')
        self.assertEqual([c.kwargs['json']['action'] for c in post.call_args_list], ['update_status', 'lock'])

    def test_type_override_wins_and_can_opt_out(self):
        self.hook()
        override = self.hook(submission_type=self.type_free, url=OTHER_URL)
        with self.capture_posts() as post:
            self.as_user(self.lab_a_admin).post(f'/api/submissions/{self.sub_free.id}/lock/')
        self.assertEqual(post.call_args.args[0], OTHER_URL)
        override.enabled = False
        override.save()
        with self.capture_posts() as post:
            self.as_user(self.lab_a_admin).post(f'/api/submissions/{self.sub_free.id}/unlock/')
        post.assert_not_called()

    def test_reads_failed_writes_and_incidental_saves_do_not_notify(self):
        self.hook()
        with self.capture_posts() as post:
            self.sub_free.save()  # e.g. assign_submissions() re-saves submissions on every login
            self.outsider.save()
            self.as_user(self.lab_a_admin).get(f'/api/submissions/{self.sub_free.id}/')
            self.as_user(self.outsider).post(f'/api/submissions/{self.sub_free.id}/lock/')
        post.assert_not_called()

    def test_url_is_rechecked_at_send_time(self):
        webhook = self.hook()
        Webhook.objects.filter(pk=webhook.pk).update(url='https://127.0.0.1/')  # e.g. DNS now points inside
        with self.capture_posts() as post:
            self.as_user(self.lab_a_admin).post(f'/api/submissions/{self.sub_free.id}/lock/')
        post.assert_not_called()
        webhook.refresh_from_db()
        self.assertIn('private', webhook.last_error)

    def test_ping_reports_only_status(self):
        webhook = self.hook()
        with self.capture_posts(status=500) as post:
            resp = self.as_user(self.lab_a_admin).post(f'/api/webhooks/{webhook.id}/ping/')
        self.assertEqual(resp.data, {'status': 500, 'error': 'HTTP 500'})
        self.assertEqual(post.call_args.kwargs['json']['event'], 'ping')

    def test_failures_are_recorded_without_echoing_the_url(self):
        webhook = self.hook()
        error = requests.ConnectionError(f'{PUBLIC_URL}?token=abc')
        with mock.patch('webhooks.delivery.requests.post', side_effect=error):
            resp = self.as_user(self.lab_a_admin).post(f'/api/webhooks/{webhook.id}/ping/')
        self.assertEqual(resp.data, {'status': None, 'error': 'ConnectionError'})
        webhook.refresh_from_db()
        self.assertEqual((webhook.last_status, webhook.last_error), (None, 'ConnectionError'))
