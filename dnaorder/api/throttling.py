"""DRF throttling classes for the dnaorder API.

Three baseline tiers (wired as DEFAULT_THROTTLE_CLASSES in settings):
  - AnonRateThrottle        -> 'anon'  (unauthenticated, keyed by client IP)
  - RegularUserRateThrottle -> 'user'  (authenticated, non lab-staff)
  - StaffRateThrottle       -> 'staff' (authenticated lab-permissioned users; generous)

Plus scoped throttles applied to specific sensitive endpoints.  Apart from login these
count per signed-in user and only apply to users without lab permissions: every user
now has to sign in, and anyone with a mailbox can, so the per-IP anonymous limits that
used to guard submission entry would no longer bite.

`is_staff` is the "has lab permissions" signal in this app: granting a lab permission sets
``user.is_staff = True`` (see ``LabViewSet.set_permissions``) and staff features gate on it
(``IsStaffPermission``). Swap to ``LabPermission.objects.filter(user=user).exists()`` if a
strict per-request check is ever preferred.
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegularUserRateThrottle(UserRateThrottle):
    """Authenticated users WITHOUT lab permissions (regular submitters/participants)."""
    scope = 'user'

    def allow_request(self, request, view):
        user = getattr(request, 'user', None)
        if not (user and user.is_authenticated):
            return True  # anonymous is handled by AnonRateThrottle
        if user.is_staff:
            return True  # lab-permissioned users are handled by StaffRateThrottle
        return super().allow_request(request, view)


class StaffRateThrottle(UserRateThrottle):
    """Authenticated users WITH lab permissions (is_staff) — generous limit."""
    scope = 'staff'

    def allow_request(self, request, view):
        user = getattr(request, 'user', None)
        if not (user and user.is_authenticated and user.is_staff):
            return True  # only applies to lab-permissioned users
        return super().allow_request(request, view)


class LoginAnonThrottle(AnonRateThrottle):
    scope = 'login'


class NonStaffScopedThrottle(UserRateThrottle):
    """A scoped limit for signed-in users without lab permissions, counted per user
    (per client IP for a request that somehow arrives unauthenticated)."""
    def allow_request(self, request, view):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and user.is_staff:
            return True  # lab-permissioned users only have the generous 'staff' tier
        return super().allow_request(request, view)


class SubmissionReadThrottle(NonStaffScopedThrottle):
    scope = 'submission_read'


class SubmissionWriteThrottle(NonStaffScopedThrottle):
    scope = 'submission_write'


class ValidateThrottle(NonStaffScopedThrottle):
    scope = 'validate'


class EmailUserThrottle(UserRateThrottle):
    """Per-user cap on endpoints that send email (applies to any authenticated user)."""
    scope = 'email'


# Apply alongside a scoped throttle so callers still fall under their per-tier baseline.
USER_TIERS = [RegularUserRateThrottle, StaffRateThrottle]


def scoped(throttle_class):
    """Build instances for ``get_throttles()``: scoped throttle + both authed tiers."""
    return [throttle_class()] + [tier() for tier in USER_TIERS]
