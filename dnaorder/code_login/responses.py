from http import HTTPStatus

from dnaorder.code_login.policy import REASON_SSO

SSO_REQUIRED = 'sso_required'
CODE_LOGIN_UNAVAILABLE = 'code_login_unavailable'

MESSAGES = {
    SSO_REQUIRED: 'This account signs in with single sign-on.',
    CODE_LOGIN_UNAVAILABLE: 'A sign-in code cannot be used for this email address. Please contact the lab.',
}


def refused_response(request, reason=REASON_SSO):
    """403 for a correct code on an account that may not use code login."""
    from allauth.headless.internal.restkit.response import APIResponse
    code = SSO_REQUIRED if reason == REASON_SSO else CODE_LOGIN_UNAVAILABLE
    return APIResponse(
        request,
        status=HTTPStatus.FORBIDDEN,
        errors=[{'message': MESSAGES[code], 'code': code}],
    )
