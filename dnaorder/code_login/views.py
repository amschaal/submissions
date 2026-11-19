"""One "email, then code" flow for known and brand-new addresses.

allauth's own code login only serves addresses that already have an account,
and its sign-up flow saves the user before the code is checked.  These two
subclasses issue a code for any address that is allowed one and create the
account only once the code has been confirmed.

They build on allauth internals (``allauth.account.internal`` and
``allauth.headless``), so django-allauth is pinned to an exact version and
``dnaorder/tests/test_code_login.py`` must pass before that pin is moved.
"""
from allauth.account.adapter import get_adapter
from allauth.account.internal.flows.login_by_code import LoginCodeVerificationProcess
from allauth.core import context, ratelimit
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.headless.account.inputs import RequestLoginCodeInput
from allauth.headless.account.views import ConfirmLoginCodeView, RequestLoginCodeView
from allauth.headless.base.response import AuthenticationResponse, ConflictResponse

from dnaorder.code_login.policy import (
    CodeLoginRefused,
    get_or_create_code_user,
    normalize_email,
    resolve_code_login,
)
from dnaorder.code_login.responses import refused_response

CODE_TEMPLATE = 'account/email/login_code'
REFUSED_TEMPLATE = 'account/email/code_login_refused'


class RequestCodeInput(RequestLoginCodeInput):
    def clean_email(self):
        email = normalize_email(self.cleaned_data['email'])
        if not ratelimit.consume(context.request, action='request_login_code', key=email):
            raise get_adapter().validation_error('too_many_login_attempts')
        self.resolution = resolve_code_login(email)
        self._user = None
        return email


class RequestCodeView(RequestLoginCodeView):
    input_class = RequestCodeInput

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return ConflictResponse(request)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = self.input.cleaned_data['email']
        resolution = self.input.resolution
        adapter = get_adapter()
        # With no user and ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS off this only stashes
        # the pending login in the session; nothing is sent yet.
        process = LoginCodeVerificationProcess.initiate(request=request, user=None, email=email)
        if resolution.allowed:
            code = process.generate_code()
            process.persist()
            adapter.send_mail(CODE_TEMPLATE, email, {'code': code})
        else:
            # No code is issued, so confirming can never succeed.  The response
            # is the same either way; the address gets a notice instead.
            adapter.send_mail(REFUSED_TEMPLATE, email, {'reason': resolution.reason})
        return AuthenticationResponse(request)


class ConfirmCodeView(ConfirmLoginCodeView):
    def post(self, request, *args, **kwargs):
        # Only reached once the submitted code matched the one that was emailed.
        try:
            user = get_or_create_code_user(self.process.state.get('email'))
        except CodeLoginRefused as refused:
            self.process.abort()
            return refused_response(request, refused.reason)
        self.stage.login.user = user
        self.process = LoginCodeVerificationProcess(stage=self.stage)
        try:
            return super().post(request, *args, **kwargs)
        except ImmediateHttpResponse as e:
            return e.response
