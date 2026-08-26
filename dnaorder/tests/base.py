"""Shared fixtures, factories and helpers for the dnaorder API test suite.

Design notes
------------
* ``MULTI_SITE`` defaults to 0, so ``get_site_institution`` resolves to
  ``Institution.objects.first()`` -- the suite therefore creates exactly one
  Institution and relies on it being first.
* ``MAP_SUBMISSION_PI`` is neutralised (set to ``None``) so creating a
  ``Submission`` never reaches out to PPMS over the network during tests.
* Throttling is disabled for functional tests by setting every throttle rate to
  ``None`` (a ``None`` rate short-circuits ``SimpleRateThrottle`` before it ever
  touches the cache).  ``test_throttling.py`` re-enables tiny rates on purpose.
* Test-client paths are literal ``/api/...`` (no ``/server`` prefix): URL
  *resolution* uses ``request.path_info`` and ignores ``FORCE_SCRIPT_NAME``,
  which only affects URL *generation* (``reverse``).
"""
import copy

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import override_settings
from rest_framework.test import APITestCase

from dnaorder.models import (
    Institution,
    InstitutionPermission,
    Lab,
    LabPermission,
    Note,
    Participant,
    PI,
    PIInstitution,
    ProjectID,
    Submission,
    SubmissionType,
)


# --- REST_FRAMEWORK copy with throttling disabled -------------------------------
_NO_THROTTLE_REST = copy.deepcopy(settings.REST_FRAMEWORK)
_NO_THROTTLE_REST["DEFAULT_THROTTLE_RATES"] = {
    scope: None for scope in _NO_THROTTLE_REST.get("DEFAULT_THROTTLE_RATES", {})
}

#: Apply to any test class that should not be affected by rate limiting or the
#: PPMS PI-mapping network call.  Use ``@no_throttle`` as a class decorator.
#: CACHES is pinned to local-memory so nothing depends on the ``throttle_cache``
#: DB table (which is created by ``createcachetable``, not a migration, and so
#: is absent from the test database).
no_throttle = override_settings(
    REST_FRAMEWORK=_NO_THROTTLE_REST,
    MAP_SUBMISSION_PI=None,
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)


# --- Factories ------------------------------------------------------------------
def make_user(username, password="pw", email="", is_superuser=False, **kwargs):
    user = User.objects.create_user(
        username=username, password=password, email=email, **kwargs
    )
    if is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()
    return user


def make_institution(institution_id="inst", name="Test Institution", site=None):
    if site is None:
        # Reuse the default Site (pk=SITE_ID) created by the sites migration so
        # get_current_site() lines up with the institution under test.
        site = Site.objects.get_or_create(
            id=settings.SITE_ID, defaults={"domain": "testserver", "name": "test"}
        )[0]
    return Institution.objects.create(id=institution_id, name=name, site=site)


def make_lab(institution, lab_id="lab-a", name="Lab A", email="lab@example.com"):
    return Lab.objects.create(
        institution=institution, lab_id=lab_id, name=name, email=email,
        payment_type_id="",
    )


def grant_lab(user, lab, permission=LabPermission.PERMISSION_MEMBER):
    """Mirror ``LabViewSet.set_permissions``: any lab permission flips is_staff."""
    LabPermission.objects.get_or_create(
        user=user, permission_object=lab, permission=permission
    )
    if not user.is_staff:
        user.is_staff = True
        user.save(update_fields=["is_staff"])
    return user


def grant_institution(user, institution, permission=InstitutionPermission.PERMISSION_ADMIN):
    InstitutionPermission.objects.get_or_create(
        user=user, permission_object=institution, permission=permission
    )
    return user


def make_submission_type(lab, name="RNA-seq", active=True, **kwargs):
    return SubmissionType.objects.create(lab=lab, name=name, active=active, **kwargs)


def make_submission(submission_type, **overrides):
    fields = dict(
        type=submission_type,
        first_name="Sub",
        last_name="Mitter",
        email="submitter@example.com",
        phone="555-0100",
        pi_first_name="Prof",
        pi_last_name="Essor",
        pi_email="pi@example.com",
        pi_phone="555-0101",
        institute="Dept of Testing",
        status=Submission.STATUS_SUBMITTED,
    )
    fields.update(overrides)
    return Submission.objects.create(**fields)


def make_participant(submission, user, roles=None):
    return Participant.objects.create(
        submission=submission, user=user, roles=roles or []
    )


def make_note(submission, text="a note", public=False, note_type=Note.TYPE_NOTE,
              created_by=None):
    return Note.objects.create(
        submission=submission, text=text, public=public, type=note_type,
        created_by=created_by,
    )


def make_project_id(lab, prefix="PRJ", next_id=1):
    return ProjectID.objects.create(lab=lab, prefix=prefix, next_id=next_id)


@no_throttle
class ApiTestCase(APITestCase):
    """Base class with a standard two-lab, multi-role fixture.

    Roles created:
      * ``superuser``        - Django superuser (bypasses everything)
      * ``inst_admin``       - institution ADMIN (not a lab member)
      * ``lab_a_admin``      - Lab A administrator (is_staff, lab member)
      * ``lab_a_member``     - Lab A member       (is_staff, lab member)
      * ``lab_a_associate``  - Lab A associate    (is_staff, NOT a lab member)
      * ``lab_b_member``     - Lab B member (for cross-tenant / IDOR tests)
      * ``outsider``         - authenticated user with no permissions anywhere

    Submissions:
      * ``sub_a``      - open (unlocked) submission in Lab A
      * ``sub_a_locked`` - locked submission in Lab A
      * ``sub_b``      - submission in Lab B
    """

    @classmethod
    def setUpTestData(cls):
        cls.institution = make_institution()
        cls.lab_a = make_lab(cls.institution, lab_id="lab-a", name="Lab A")
        cls.lab_b = make_lab(cls.institution, lab_id="lab-b", name="Lab B")

        cls.superuser = make_user("root", is_superuser=True, email="root@example.com")
        cls.inst_admin = grant_institution(
            make_user("inst_admin", email="ia@example.com"), cls.institution
        )
        cls.lab_a_admin = grant_lab(
            make_user("lab_a_admin", email="aadmin@example.com"), cls.lab_a,
            LabPermission.PERMISSION_ADMIN,
        )
        cls.lab_a_member = grant_lab(
            make_user("lab_a_member", email="amember@example.com"), cls.lab_a,
            LabPermission.PERMISSION_MEMBER,
        )
        cls.lab_a_associate = grant_lab(
            make_user("lab_a_assoc", email="aassoc@example.com"), cls.lab_a,
            LabPermission.PERMISSION_ASSOCIATE,
        )
        cls.lab_b_member = grant_lab(
            make_user("lab_b_member", email="bmember@example.com"), cls.lab_b,
            LabPermission.PERMISSION_MEMBER,
        )
        cls.outsider = make_user("outsider", email="out@example.com")

        cls.type_a = make_submission_type(cls.lab_a, name="Lab A Type")
        cls.type_b = make_submission_type(cls.lab_b, name="Lab B Type")

        cls.sub_a = make_submission(cls.type_a, first_name="Alpha")
        cls.sub_a_locked = make_submission(cls.type_a, first_name="Locked", locked=True)
        cls.sub_b = make_submission(cls.type_b, first_name="Bravo")

    # -- helpers ---------------------------------------------------------------
    def as_user(self, user):
        self.client.force_authenticate(user=user)
        return self.client

    def as_anon(self):
        self.client.force_authenticate(user=None)
        return self.client

    def assertDenied(self, response, msg=None):
        """Auth/permission denial is 401 or 403 depending on authenticator."""
        self.assertIn(
            response.status_code, (401, 403),
            msg or "expected 401/403, got {}: {}".format(
                response.status_code, getattr(response, "data", b"")),
        )
