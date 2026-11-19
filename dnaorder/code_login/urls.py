"""Only the two code-login endpoints are exposed.

Do not include ``allauth.urls`` or ``allauth.headless.urls``: their sign-up,
password and email-management endpoints are not part of this app's login model.
"""
from allauth.headless.constants import Client
from django.urls import path

from dnaorder.code_login import views

urlpatterns = [
    path(
        'browser/v1/auth/code/request',
        views.RequestCodeView.as_api_view(client=Client.BROWSER),
        name='request_login_code',
    ),
    path(
        'browser/v1/auth/code/confirm',
        views.ConfirmCodeView.as_api_view(client=Client.BROWSER),
        name='confirm_login_code',
    ),
]
