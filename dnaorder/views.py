from django.shortcuts import redirect
from dnaorder.models import SubmissionType, Submission, UserEmail
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from dnaorder.api.serializers import UserSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from dnaorder.validators import SamplesheetValidator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny
from dnaorder.api.throttling import (
    LoginAnonThrottle, ValidateAnonThrottle, SubmissionReadAnonThrottle, USER_TIERS,
)
from dnaorder.spreadsheets import (
    dataset_response,
    get_dataset,
    get_submission_dataset,
    get_cols,
)
import tablib
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlencode


def login(request):
    if hasattr(settings, "SOCIAL_LOGIN_URL"):
        return redirect(settings.SOCIAL_LOGIN_URL)
    print("process request", request.META)
    print("login", request.user)
    if request.user.is_authenticated:
        print("is authenticated")
        return redirect("/submissions/")
    else:
        print("authenticate?", request.META)
        # Should probably be relying on REMOTE USER using the following config in apache
        # OIDCRemoteUserClaim preferred_username
        remote_user = request.META.get(
            "OIDC_CLAIM_preferred_username", request.META.get("OIDC_CLAIM_email")
        )
        print("remote_user", remote_user)
        if remote_user:
            user, created = User.objects.get_or_create(username=remote_user)
            if created:
                print("user created")
                user.email = request.META.get("OIDC_CLAIM_email")
                user.last_name = request.META.get("OIDC_CLAIM_family_name")
                user.first_name = request.META.get("OIDC_CLAIM_given_name")
                user.save()
                UserEmail.objects.create(user=user, email=user.email)
            auth_login(request, user)
            return redirect("/")
    return redirect("/")


def logout(request):
    print("logout", request.user)
    if request.user.is_authenticated:
        auth_logout(request)
    site = get_current_site(request)
    return redirect(
        "/server/accounts/login/redirect?logout=https://{}/".format(site.domain)
    )


@api_view(["POST"])
@csrf_exempt
@permission_classes((AllowAny,))
@throttle_classes([LoginAnonThrottle])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if request.user.is_authenticated and not username:
        user = request.user
    else:
        user = authenticate(request._request, username=username, password=password)
    if user is not None:
        auth_login(request._request, user)
        return Response(
            {"status": "success", "user": UserSerializer(instance=user).data}
        )
    else:
        return Response({"message": "Authentication failed."}, status=400)


# The SPA calls this on boot, so it doubles as the point where we hand the
# browser a CSRF cookie -- without it the logout POST (and any other write)
# made right after a social login would be rejected.
@ensure_csrf_cookie
@api_view(["GET"])
@csrf_exempt
@permission_classes((AllowAny,))
def get_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response(
            {"status": "success", "user": UserSerializer(instance=user).data}
        )
    else:
        return Response({"message": "Not authenticated."}, status=403)


def keycloak_logout_url(request):
    """URL that ends the Keycloak SSO session and returns the browser to us.

    Keycloak 18+ expects client_id + post_logout_redirect_uri, older releases
    used redirect_uri; we send both so either version behaves, since each
    ignores the parameter it does not know.
    """
    end_session_url = getattr(settings, "SOCIAL_AUTH_KEYCLOAK_END_SESSION_URL", None)
    if not end_session_url:
        return None
    redirect_url = getattr(
        settings, "POST_LOGOUT_REDIRECT_URL", None
    ) or request.build_absolute_uri("/")
    params = urlencode(
        {
            "client_id": settings.SOCIAL_AUTH_KEYCLOAK_KEY,
            "post_logout_redirect_uri": redirect_url,
            "redirect_uri": redirect_url,
        }
    )
    return "{}?{}".format(end_session_url, params)


@api_view(["POST"])
def logout_view(request):
    # Django's session is only half of it: a user who signed in through
    # Keycloak keeps their SSO session there and would be signed straight back
    # in, so hand the SPA a URL to finish the job.  Both reads have to happen
    # before auth_logout flushes the session.
    keycloak_url = (
        keycloak_logout_url(request)
        if request.user.is_authenticated and request.user.social_auth.exists()
        else None
    )
    auth_logout(request)
    return Response({"status": "success", "redirect_url": keycloak_url or "/"})


@api_view(["POST"])
@permission_classes((AllowAny,))
@throttle_classes([ValidateAnonThrottle, *USER_TIERS])
def validate_data(request, type_id=None):
    if type_id:
        schema = SubmissionType.objects.get(id=type).sample_schema
    else:
        schema = request.data.get("sample_schema")
    validator = SamplesheetValidator(schema, request.data.get("data"))
    errors, warnings = (
        validator.validate()
    )  # validate_samplesheet(submission_type.schema,request.data.get('data'))
    if len(errors) == 0 and len(warnings) == 0:
        return Response(
            {"status": "success", "message": "The data was successfully validated"}
        )
    else:
        return Response({"errors": errors, "warnings": warnings}, status=400)


@api_view(["GET"])
@permission_classes((AllowAny,))
@throttle_classes([SubmissionReadAnonThrottle, *USER_TIERS])
def download(request, id):
    submission = Submission.objects.get(id=id)
    data = request.GET.get("data", "combined")  # samples or submission
    # Read the export format from `export_format`, not `format`: this is a DRF
    # @api_view, and DRF content negotiation claims a `?format=` query param
    # (URL_FORMAT_OVERRIDE) — a value like xlsx/tsv/csv matches no configured
    # renderer and 404s before this view runs. The list/report exports use the
    # same `export_format` convention.
    format = request.GET.get("export_format", "xlsx")
    format = format if format in ["xls", "xlsx", "csv", "tsv", "json"] else "xlsx"
    filename = None

    if data == "submission":
        dataset = get_submission_dataset(submission)
        prefix = "{0}.submission".format(submission.internal_id or submission.id)
    elif data == "all":  # samples
        submission_data = get_submission_dataset(submission)
        submission_data.title = "Submission"
        table_cols = get_cols(submission.submission_schema, table=True)
        tables = [submission_data]
        for col in table_cols:
            table_data = get_dataset(
                submission.submission_schema.get("properties", {})
                .get(col, {})
                .get("schema", {}),
                submission.submission_data.get(col, []),
            )
            table_data.title = col
            tables.append(table_data)
        dataset = tablib.Databook(tables)
        format = "xlsx"
        prefix = submission.internal_id or submission.id
    else:  # all
        dataset = get_dataset(
            submission.submission_schema.get("properties", {})
            .get(data, {})
            .get("schema", {}),
            submission.submission_data.get(data, []),
        )
        dataset.title = data
        prefix = "{0}.{1}".format(submission.internal_id or submission.id, data)
    return dataset_response(dataset, prefix, format)
    # generate the file


#     return sendfile(request, file_path, attachment_filename=filename,attachment=True)


@api_view(["GET"])
@csrf_exempt
@permission_classes((AllowAny,))
def test(request):
    return Response({"message": "Test message"})
