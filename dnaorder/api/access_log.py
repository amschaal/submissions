"""Record requests that reach a submission the caller is not entitled to open.

Logged at WARNING to ``dnaorder.access`` so the lines show up in the container
log without any logging configuration.  Nothing is refused here.
"""
import logging

from rest_framework.authtoken.models import Token

logger = logging.getLogger('dnaorder.access')


def auth_type(request):
    if not request.user.is_authenticated:
        return 'anonymous'
    return 'token' if isinstance(getattr(request, 'auth', None), Token) else 'session'


def log_unlisted_access(request, submission):
    """Log when ``request.user`` is not someone ``Submission.objects.visible_to``
    would return ``submission`` for (not signed in, or not named on it and not staff)."""
    if submission is None or submission.is_visible_to(request.user):
        return
    logger.warning(
        'unlisted submission access: user=%s auth=%s method=%s path=%s submission=%s',
        request.user.username if request.user.is_authenticated else '-',
        auth_type(request), request.method, request.path, submission.pk,
    )
