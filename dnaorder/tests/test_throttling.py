"""DRF throttling is actually enforced (returns HTTP 429).

IMPORTANT: DRF captures ``SimpleRateThrottle.THROTTLE_RATES`` at import time from
``api_settings.DEFAULT_THROTTLE_RATES``, so ``override_settings(REST_FRAMEWORK=...)``
does NOT change the effective rates. We therefore patch that class dict directly
to tiny rates so a limit trips on the second request. A local-memory cache backs
the counters, cleared per test for isolation.

Does NOT inherit from ``ApiTestCase``; it builds its own minimal fixture.
"""
from unittest import mock

from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework.throttling import SimpleRateThrottle

from dnaorder.tests.base import (
    make_institution, make_lab, make_submission, make_submission_type, make_user,
)

_LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

_LOW_RATES = {
    "login": "1/min",
    "submission_read": "1/min",
    "user": "1/min",
    "anon": "1/min",
}


@override_settings(CACHES=_LOCMEM, MAP_SUBMISSION_PI=None)
class ThrottlingTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.institution = make_institution()
        cls.lab = make_lab(cls.institution)
        cls.type = make_submission_type(cls.lab)
        cls.sub = make_submission(cls.type)
        cls.user = make_user("throttle_user", password="pw", email="t@example.com")

    def setUp(self):
        cache.clear()  # isolate throttle counters between tests
        # Patch the import-captured rate table so overrides actually take effect.
        patcher = mock.patch.dict(SimpleRateThrottle.THROTTLE_RATES, _LOW_RATES)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_login_endpoint_is_rate_limited(self):
        url = "/api/login/"
        first = self.client.post(url, {"username": "x", "password": "y"}, format="json")
        self.assertNotEqual(first.status_code, 429)
        second = self.client.post(url, {"username": "x", "password": "y"}, format="json")
        self.assertEqual(second.status_code, 429, second.content)
        self.assertIn("Retry-After", second)

    def test_open_submission_read_is_rate_limited_for_anonymous(self):
        url = "/api/submissions/{}/".format(self.sub.id)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 429)

    def test_authenticated_user_tier_is_rate_limited(self):
        self.client.force_authenticate(user=self.user)
        url = "/api/submissions/"
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 429)

    def test_counter_is_per_scope_not_global(self):
        # Tripping the login limit must not throttle an unrelated read scope.
        self.client.post("/api/login/", {"username": "x", "password": "y"}, format="json")
        self.client.post("/api/login/", {"username": "x", "password": "y"}, format="json")
        # submission_read scope is still fresh:
        self.assertEqual(self.client.get("/api/submissions/{}/".format(self.sub.id)).status_code, 200)
