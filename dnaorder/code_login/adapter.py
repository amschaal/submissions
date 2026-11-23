from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.core import context as allauth_context
from allauth.core.exceptions import ImmediateHttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_str
from rest_framework.settings import api_settings

from dnaorder.code_login.policy import REASON_SSO, REASON_UNAVAILABLE, is_privileged
from dnaorder.code_login.responses import refused_response
from dnaorder.utils import get_site_institution


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Accounts are only created by confirming a code (see views.ConfirmCodeView).
        return False

    def add_message(self, *args, **kwargs):
        # The SPA never renders Django messages; don't let them pile up in the session.
        pass

    def pre_login(self, request, user, **kwargs):
        """Every allauth login passes through here: lab staff, institution
        admins and superusers must use single sign-on instead."""
        if not user.is_active or is_privileged(user):
            from allauth.account.internal.stagekit import clear_login
            clear_login(request)
            reason = REASON_SSO if is_privileged(user) else REASON_UNAVAILABLE
            raise ImmediateHttpResponse(refused_response(request, reason))
        return super().pre_login(request, user, **kwargs)

    def login(self, request, user):
        # allauth would otherwise pick the first configured backend (Keycloak).
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        super().login(request, user)
        # A code has to be waited for, so these sessions last longer than the default.
        request.session.set_expiry(settings.CODE_LOGIN_SESSION_AGE)

    # -- email -----------------------------------------------------------------
    def _institution(self):
        try:
            return get_site_institution(allauth_context.request)
        except Exception:
            return None

    def get_from_email(self):
        institution = self._institution()
        return institution.from_email() if institution else settings.DEFAULT_FROM_EMAIL

    def format_email_subject(self, subject):
        return force_str(subject)

    def send_mail(self, template_prefix, email, context):
        ctx = {
            'institution': self._institution(),
            'code_minutes': max(1, app_settings.LOGIN_BY_CODE_TIMEOUT // 60),
        }
        ctx.update(context)
        super().send_mail(template_prefix, email, ctx)

    # -- rate limiting ---------------------------------------------------------
    def get_client_ip(self, request):
        """Same client address the DRF throttles use (REST_FRAMEWORK['NUM_PROXIES']),
        so both sets of limits agree on who the client is behind the proxy."""
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        num_proxies = api_settings.NUM_PROXIES
        if num_proxies is not None and num_proxies > 0 and xff:
            addrs = xff.split(',')
            ip = addrs[-min(num_proxies, len(addrs))].strip()
        else:
            ip = remote_addr
        if not ip:
            raise PermissionDenied('Unable to determine client IP address')
        return ip
