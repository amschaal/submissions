"""Only the login backends the app uses are configured and routable."""
from django.conf import settings
from django.test import TestCase


class LoginBackendTests(TestCase):
    def test_only_expected_backends_are_configured(self):
        self.assertEqual(
            set(settings.AUTHENTICATION_BACKENDS),
            {
                "social_core.backends.keycloak.KeycloakOAuth2",
                "django.contrib.auth.backends.ModelBackend",
            },
        )

    def test_unused_backend_routes_are_not_found(self):
        self.assertEqual(self.client.post("/social/login/openid/").status_code, 404)
        self.assertEqual(self.client.get("/social/complete/openid/").status_code, 404)

    def test_keycloak_login_route_still_resolves(self):
        # Redirects to Keycloak (or errors on missing config), but is not a 404.
        resp = self.client.post("/social/login/keycloak/")
        self.assertNotEqual(resp.status_code, 404)
