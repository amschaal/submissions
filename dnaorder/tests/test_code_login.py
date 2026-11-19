"""Emailed one-time-code login (``dnaorder/code_login``).

These tests also guard the django-allauth pin: the two views subclass allauth's
headless code-login views and use its internal login process, so they must pass
before the pinned version is changed.

The allauth endpoints are plain Django views driven by the session, so the
tests use real sessions (no ``force_authenticate``).
"""
import re
from io import StringIO
from unittest import mock

from allauth.account.models import EmailAddress
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import RequestFactory, override_settings
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from dnaorder.code_login.adapter import AccountAdapter
from dnaorder.models import UserEmail
from dnaorder.tests.base import ApiTestCase, grant_lab, make_submission, make_user
from dnaorder.views import KEYCLOAK_BACKEND

REQUEST = "/_allauth/browser/v1/auth/code/request"
CONFIRM = "/_allauth/browser/v1/auth/code/confirm"
MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"


class CodeLoginTestCase(ApiTestCase):
    def request_code(self, email, client=None):
        return (client or self.client).post(REQUEST, {"email": email}, format="json")

    def confirm(self, code, client=None):
        return (client or self.client).post(CONFIRM, {"code": code}, format="json")

    def emailed_code(self):
        """The code in the most recent email, or None if it carries no code."""
        match = re.search(r"^\d{6}$", mail.outbox[-1].body, re.M)
        return match.group(0) if match else None

    def wrong_code(self, code):
        return "000000" if code != "000000" else "111111"

    def sign_in(self, email, client=None):
        resp = self.request_code(email, client)
        self.assertEqual(resp.status_code, 401, resp.content)
        return self.confirm(self.emailed_code(), client)

    def error_codes(self, resp):
        return [error.get("code") for error in resp.json().get("errors", [])]

    def assertSignedOut(self, client=None):
        self.assertEqual((client or self.client).get("/api/get_user/").status_code, 403)


class NewAddressTests(CodeLoginTestCase):
    EMAIL = "newcomer@example.com"

    def test_request_sends_a_code_but_creates_no_account(self):
        users_before = User.objects.count()
        resp = self.request_code(self.EMAIL)
        self.assertEqual(resp.status_code, 401, resp.content)
        flows = {flow["id"]: flow for flow in resp.json()["data"]["flows"]}
        self.assertTrue(flows["login_by_code"]["is_pending"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.EMAIL])
        self.assertIsNotNone(self.emailed_code())
        self.assertEqual(User.objects.count(), users_before)
        self.assertFalse(EmailAddress.objects.filter(email__iexact=self.EMAIL).exists())
        self.assertSignedOut()

    def test_email_is_plain_text_from_the_institution(self):
        self.request_code(self.EMAIL)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, self.institution.from_email())
        self.assertIn(self.institution.name, message.subject)
        self.assertIn("expires in 10 minutes", message.body)
        self.assertEqual(getattr(message, "alternatives", []), [])

    def test_confirm_creates_the_account_and_signs_in(self):
        resp = self.sign_in(self.EMAIL)
        self.assertEqual(resp.status_code, 200, resp.content)
        user = User.objects.get(email=self.EMAIL)
        self.assertEqual(user.username, self.EMAIL)
        self.assertFalse(user.has_usable_password())
        self.assertFalse(user.is_staff)
        address = EmailAddress.objects.get(user=user)
        self.assertTrue(address.verified)
        self.assertTrue(address.primary)
        me = self.client.get("/api/get_user/")
        self.assertEqual(me.status_code, 200, me.content)
        self.assertEqual(me.data["user"]["email"], self.EMAIL)
        self.assertEqual(self.client.session[BACKEND_SESSION_KEY], MODEL_BACKEND)

    def test_address_is_normalised(self):
        resp = self.request_code("  NewComer@Example.com ")
        self.assertEqual(resp.status_code, 401, resp.content)
        self.assertEqual(self.confirm(self.emailed_code()).status_code, 200)
        self.assertTrue(User.objects.filter(email=self.EMAIL).exists())

    def test_submissions_are_attached_only_once_the_code_is_confirmed(self):
        submission = make_submission(self.type_a, email="Fresh@Example.com")  # no account yet
        self.request_code("fresh@example.com")
        self.assertEqual(submission.users.count(), 0)
        self.assertEqual(self.confirm(self.emailed_code()).status_code, 200)
        user = User.objects.get(email="fresh@example.com")
        self.assertIn(user, submission.users.all())
        mine = self.client.get("/api/submissions/")
        self.assertEqual([row["id"] for row in mine.data["results"]], [submission.id])
        self.assertEqual(self.client.get("/api/submissions/{}/".format(submission.id)).status_code, 200)
        self.assertEqual(self.client.get("/api/submissions/{}/".format(self.sub_b.id)).status_code, 404)

    def test_keycloak_pipeline_finds_the_code_created_account(self):
        from social_django.models import DjangoStorage
        self.assertEqual(self.sign_in(self.EMAIL).status_code, 200)
        user = User.objects.get(email=self.EMAIL)
        self.assertEqual(list(DjangoStorage.user.get_users_by_email(self.EMAIL)), [user])


class ExistingAccountTests(CodeLoginTestCase):
    def test_existing_non_staff_user_signs_into_the_same_account(self):
        users_before = User.objects.count()
        resp = self.sign_in(self.outsider.email)
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(User.objects.count(), users_before)
        self.assertEqual(self.client.get("/api/get_user/").data["user"]["id"], self.outsider.id)
        self.assertTrue(
            EmailAddress.objects.filter(user=self.outsider, email=self.outsider.email, verified=True).exists()
        )

    def test_mixed_case_stored_email_matches(self):
        user = make_user("mixed", email="Mixed.Case@Example.com")
        resp = self.sign_in("mixed.case@example.com")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(self.client.get("/api/get_user/").data["user"]["id"], user.id)
        self.assertEqual(User.objects.filter(email__iexact="mixed.case@example.com").count(), 1)

    def test_confirmed_secondary_address_signs_into_its_owner(self):
        UserEmail.objects.create(user=self.outsider, email="second@example.com")
        resp = self.sign_in("second@example.com")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(self.client.get("/api/get_user/").data["user"]["id"], self.outsider.id)
        self.assertFalse(User.objects.filter(email="second@example.com").exists())

    def test_request_while_signed_in_is_a_conflict(self):
        self.client.force_login(self.outsider, backend=MODEL_BACKEND)
        self.assertEqual(self.request_code("other@example.com").status_code, 409)
        self.assertEqual(len(mail.outbox), 0)


class RefusalTests(CodeLoginTestCase):
    """Accounts that must not sign in by code look exactly like any other
    address to the caller, and never receive a code."""

    def refused_addresses(self):
        make_user("stale_staff", email="stale@example.com", is_staff=True)
        make_user("gone", email="gone@example.com", is_active=False)
        make_user("dup1", email="dup@example.com")
        make_user("dup2", email="Dup@example.com")
        return {
            "lab member": self.lab_a_member.email,
            "lab associate": self.lab_a_associate.email,
            "superuser": self.superuser.email,
            "institution admin without is_staff": self.inst_admin.email,
            "is_staff without permissions": "stale@example.com",
            "inactive account": "gone@example.com",
            "address shared by two accounts": "dup@example.com",
        }

    def test_refused_addresses_are_indistinguishable_and_get_no_code(self):
        baseline = self.request_code("nobody@example.com").json()
        users_before = User.objects.count()
        for label, email in self.refused_addresses().items():
            with self.subTest(label):
                cache.clear()  # keep the per-IP request limit out of this test
                client = APIClient()
                mail.outbox.clear()
                resp = self.request_code(email, client)
                self.assertEqual(resp.status_code, 401, resp.content)
                self.assertEqual(resp.json(), baseline)
                self.assertEqual(len(mail.outbox), 1)
                self.assertEqual(mail.outbox[0].to, [email])
                self.assertIsNone(re.search(r"\b\d{6}\b", mail.outbox[0].body))
                wrong = self.confirm("123456", client)
                self.assertEqual(wrong.status_code, 400, wrong.content)
                self.assertEqual(self.error_codes(wrong), ["incorrect_code"])
                self.assertSignedOut(client)
        self.assertEqual(User.objects.count(), users_before + 4)  # only the fixtures above

    def test_staff_notice_points_to_single_sign_on(self):
        self.request_code(self.lab_a_member.email)
        self.assertIn("single sign-on", mail.outbox[0].body)

    def test_account_promoted_after_the_code_was_sent_is_refused(self):
        self.request_code(self.outsider.email)
        code = self.emailed_code()
        grant_lab(self.outsider, self.lab_a)
        resp = self.confirm(code)
        self.assertEqual(resp.status_code, 403, resp.content)
        self.assertEqual(self.error_codes(resp), ["sso_required"])
        self.assertSignedOut()
        self.assertEqual(self.confirm(code).status_code, 409)


class CodeLifecycleTests(CodeLoginTestCase):
    EMAIL = "lifecycle@example.com"

    def test_three_wrong_codes_end_the_attempt(self):
        self.request_code(self.EMAIL)
        code = self.emailed_code()
        for _ in range(3):
            resp = self.confirm(self.wrong_code(code))
            self.assertEqual(resp.status_code, 400, resp.content)
            self.assertEqual(self.error_codes(resp), ["incorrect_code"])
        self.assertEqual(self.confirm(code).status_code, 409)
        self.assertSignedOut()
        self.assertFalse(User.objects.filter(email=self.EMAIL).exists())

    def test_wrong_then_right_code_signs_in(self):
        self.request_code(self.EMAIL)
        code = self.emailed_code()
        self.assertEqual(self.confirm(self.wrong_code(code)).status_code, 400)
        self.assertEqual(self.confirm(code).status_code, 200)

    @override_settings(ACCOUNT_LOGIN_BY_CODE_TIMEOUT=-1)
    def test_expired_code_is_rejected(self):
        self.request_code(self.EMAIL)
        self.assertEqual(self.confirm(self.emailed_code()).status_code, 409)
        self.assertSignedOut()

    def test_code_only_works_in_the_browser_that_requested_it(self):
        self.request_code(self.EMAIL)
        other = APIClient()
        self.assertEqual(self.confirm(self.emailed_code(), other).status_code, 409)
        self.assertSignedOut(other)

    def test_code_cannot_be_used_twice(self):
        self.request_code(self.EMAIL)
        code = self.emailed_code()
        self.assertEqual(self.confirm(code).status_code, 200)
        self.client.logout()
        self.assertEqual(self.confirm(code).status_code, 409)

    def test_new_request_replaces_the_previous_code(self):
        self.request_code(self.EMAIL)
        first = self.emailed_code()
        self.request_code(self.EMAIL)
        second = self.emailed_code()
        if first != second:
            self.assertEqual(self.confirm(first).status_code, 400)
        self.assertEqual(self.confirm(second).status_code, 200)

    def test_requests_for_one_address_are_rate_limited(self):
        for _ in range(3):
            self.assertEqual(self.request_code(self.EMAIL, APIClient()).status_code, 401)
        resp = self.request_code(self.EMAIL, APIClient())
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertEqual(self.error_codes(resp), ["too_many_login_attempts"])
        self.assertEqual(len(mail.outbox), 3)

    def test_invalid_email_is_a_field_error(self):
        resp = self.request_code("not-an-email")
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertEqual(resp.json()["errors"][0]["param"], "email")
        self.assertEqual(len(mail.outbox), 0)

    def test_csrf_is_enforced(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertEqual(self.request_code(self.EMAIL, client).status_code, 403)
        self.assertEqual(len(mail.outbox), 0)


class EndpointSurfaceTests(CodeLoginTestCase):
    def test_only_the_two_code_endpoints_are_mounted(self):
        for path in [
            "/_allauth/browser/v1/auth/signup",
            "/_allauth/browser/v1/auth/login",
            "/_allauth/browser/v1/auth/session",
            "/_allauth/browser/v1/auth/code/resend",
            "/_allauth/browser/v1/auth/password/request",
            "/_allauth/browser/v1/auth/password/reset",
            "/_allauth/browser/v1/auth/email/verify",
            "/_allauth/browser/v1/account/email",
            "/_allauth/browser/v1/account/password/change",
            "/_allauth/browser/v1/config",
            "/_allauth/app/v1/auth/code/request",
            "/_allauth/app/v1/auth/code/confirm",
        ]:
            with self.subTest(path):
                self.assertEqual(self.client.post(path, {}, format="json").status_code, 404)
                self.assertEqual(self.client.get(path).status_code, 404)


@override_settings(SOCIAL_AUTH_KEYCLOAK_END_SESSION_URL="https://sso.example.com/logout")
class LogoutTests(CodeLoginTestCase):
    def test_code_session_logs_out_locally(self):
        self.assertEqual(self.sign_in("leaver@example.com").status_code, 200)
        resp = self.client.post("/api/logout/", {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["redirect_url"], "/")
        self.assertSignedOut()

    def test_single_sign_on_session_is_sent_to_end_the_sso_session(self):
        self.client.force_login(self.lab_a_member, backend=KEYCLOAK_BACKEND)
        resp = self.client.post("/api/logout/", {}, format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertTrue(resp.data["redirect_url"].startswith("https://sso.example.com/logout?"))


class ClientIpTests(CodeLoginTestCase):
    def ip(self, num_proxies, **meta):
        request = RequestFactory().post(REQUEST, **meta)
        with mock.patch.object(api_settings, "NUM_PROXIES", num_proxies):
            return AccountAdapter().get_client_ip(request)

    def test_uses_remote_addr_without_forwarding(self):
        self.assertEqual(self.ip(2, REMOTE_ADDR="10.0.0.9"), "10.0.0.9")

    def test_counts_proxies_from_the_right(self):
        xff = "203.0.113.7, 198.51.100.2, 10.0.0.1"
        self.assertEqual(self.ip(1, REMOTE_ADDR="10.0.0.9", HTTP_X_FORWARDED_FOR=xff), "10.0.0.1")
        self.assertEqual(self.ip(2, REMOTE_ADDR="10.0.0.9", HTTP_X_FORWARDED_FOR=xff), "198.51.100.2")

    def test_short_forwarding_chain_does_not_error(self):
        self.assertEqual(self.ip(2, REMOTE_ADDR="10.0.0.9", HTTP_X_FORWARDED_FOR="203.0.113.7"), "203.0.113.7")

    def test_ignores_forwarding_header_when_no_proxy_is_trusted(self):
        self.assertEqual(self.ip(0, REMOTE_ADDR="10.0.0.9", HTTP_X_FORWARDED_FOR="203.0.113.7"), "10.0.0.9")


class EmailClaimTests(CodeLoginTestCase):
    def test_cannot_claim_another_accounts_sign_in_address(self):
        resp = self.as_user(self.outsider).post(
            "/api/emails/claim/", {"email": self.lab_a_member.email.upper()}, format="json"
        )
        self.assertEqual(resp.status_code, 403, resp.content)
        self.assertEqual(len(mail.outbox), 0)

    def test_can_still_claim_an_unused_address(self):
        resp = self.as_user(self.outsider).post(
            "/api/emails/claim/", {"email": "unused@example.com"}, format="json"
        )
        self.assertEqual(resp.status_code, 200, resp.content)


class CheckLoginEmailsCommandTests(CodeLoginTestCase):
    def run_command(self, *args):
        out = StringIO()
        call_command("check_login_emails", *args, stdout=out)
        return out.getvalue()

    def test_clean_data_reports_nothing_shared(self):
        output = self.run_command("--fail-on-duplicates")
        self.assertIn("Addresses tied to more than one account: 0", output)

    def test_reports_shared_addresses_and_stale_staff(self):
        make_user("twin", email=self.lab_a_member.email.upper())
        make_user("stale_staff", email="stale@example.com", is_staff=True)
        output = self.run_command()
        self.assertIn("Addresses tied to more than one account: 1", output)
        self.assertIn(self.lab_a_member.email, output)
        self.assertIn("shared between a staff and a non-staff account", output)
        self.assertIn("username=stale_staff", output)
        with self.assertRaises(CommandError):
            self.run_command("--fail-on-duplicates")
