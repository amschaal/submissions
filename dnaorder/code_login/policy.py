"""Who may sign in with an emailed code, and which account a code signs into."""
from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower

#: The address belongs to an account that must use single sign-on.
REASON_SSO = 'sso'
#: The address cannot be used for code login (inactive or ambiguous account).
REASON_UNAVAILABLE = 'unavailable'

USERNAME_MAX_LENGTH = User._meta.get_field('username').max_length


class CodeLoginRefused(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class Resolution:
    """Outcome of looking an email address up for code login.

    ``allowed`` with ``user=None`` means the address is unknown and an account
    will be created once a code has been confirmed.
    """
    allowed: bool
    user: Optional[User] = None
    reason: Optional[str] = None


def normalize_email(email):
    return (email or '').strip().lower()


def is_privileged(user):
    """Staff, superusers and anyone holding a lab or institution permission."""
    from dnaorder.models import InstitutionPermission, LabPermission
    return bool(
        user.is_staff
        or user.is_superuser
        or LabPermission.objects.filter(user=user).exists()
        or InstitutionPermission.objects.filter(user=user).exists()
    )


def is_supported_address(email):
    """Sign-in codes are only sent to plain ASCII addresses."""
    return (email or '').isascii()


def _matching(queryset, email):
    """Rows whose address equals ``email``, ignoring case: both sides are
    lower-cased, the way ``Submission.objects.named`` and
    ``dnaorder.utils.assign_submission`` compare addresses.

    ``email`` must already be normalized.
    """
    return queryset.alias(lower_email=Lower('email')).filter(lower_email=email)


def users_for_email(email):
    """Every account the address is tied to: as its primary email, as a
    confirmed secondary email, or as an address verified by a previous code login."""
    from allauth.account.models import EmailAddress
    from dnaorder.models import UserEmail
    email = normalize_email(email)
    if not email:
        return []
    ids = set(_matching(User.objects, email).values_list('pk', flat=True))
    ids.update(_matching(UserEmail.objects, email).values_list('user_id', flat=True))
    ids.update(_matching(EmailAddress.objects.filter(verified=True), email).values_list('user_id', flat=True))
    return list(User.objects.filter(pk__in=ids))


def resolve_code_login(email):
    if not is_supported_address(email):
        return Resolution(allowed=False, reason=REASON_UNAVAILABLE)
    users = users_for_email(email)
    if not users:
        return Resolution(allowed=True)
    if any(is_privileged(user) for user in users):
        return Resolution(allowed=False, reason=REASON_SSO)
    if len(users) > 1 or not users[0].is_active:
        return Resolution(allowed=False, reason=REASON_UNAVAILABLE)
    return Resolution(allowed=True, user=users[0])


def _username_for(email):
    """The email address itself where Django accepts it as a username, so it
    cannot collide with a single sign-on username."""
    try:
        UnicodeUsernameValidator()(email)
        usable = len(email) <= USERNAME_MAX_LENGTH
    except ValidationError:
        usable = False
    if usable and not User.objects.filter(username__iexact=email).exists():
        return email
    from allauth.account.adapter import get_adapter
    return get_adapter().generate_unique_username([email.split('@')[0], 'user'])


def _create_user(email):
    user = User(username=_username_for(email), email=email)
    user.set_unusable_password()
    user.save()
    return user


def _record_verified_email(user, email):
    from allauth.account.models import EmailAddress
    address = _matching(EmailAddress.objects.filter(user=user), email).first()
    if address is None:
        is_primary = (
            normalize_email(user.email) == email
            and not EmailAddress.objects.filter(user=user, primary=True).exists()
        )
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=is_primary)
    elif not address.verified:
        address.verified = True
        address.save(update_fields=['verified'])


def get_or_create_code_user(email):
    """Return the account a confirmed code for ``email`` signs into, creating
    it if the address is new.  Only call this once the code has been verified:
    saving a user with an email attaches them to that address's submissions.

    Raises ``CodeLoginRefused`` if the address may not use code login.
    """
    email = normalize_email(email)
    for attempt in range(2):
        resolution = resolve_code_login(email)
        if not resolution.allowed:
            raise CodeLoginRefused(resolution.reason)
        try:
            with transaction.atomic():
                user = resolution.user or _create_user(email)
                _record_verified_email(user, email)
            return user
        except IntegrityError:
            # Lost a race with another request for the same address: look again.
            if attempt:
                raise
