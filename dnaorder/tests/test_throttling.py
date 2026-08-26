"""DRF throttling is actually enforced (returns HTTP 429).

Runs with tiny per-scope rates and a local-memory cache so limits trip on the
second request.  Deliberately does NOT inherit from ``ApiTestCase`` (which
disables throttling); it builds its own minimal fixture instead.
"""
import copy

from django.conf import settings
from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase

from dnaorder.tests.base import (
    make_institution, make_lab, make_submission, make_submission_type, make_user,
)

_RF = copy.deepcopy(settings.REST_FRAMEWORK)
_RF["DEFAULT_THROTTLE_RATES"] = {
    **_RF["DEFAULT_THROTTLE_RATES"],
    "login": "1/min",
    "submission_read": "1/min",
    "user": "1/min",
    "anon": "1/min",
}
_RF["NUM_PROXIES"] = 0  # key throttles directly on REMOTE_ADDR in tests

_LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


@override_settings(REST_FRAMEWORK=_RF, CACHES=_LOCMEM, MAP_SUBMISSION_PI=None)
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
