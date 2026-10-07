"""Fire-and-forget webhook delivery of a small submission event, guarded against SSRF."""
import ipaddress
import logging
import socket
import threading
import uuid
from urllib.parse import urlsplit

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.urls import get_script_prefix
from django.utils import timezone

from dnaorder.utils import get_lab_uri
from webhooks.models import Webhook

logger = logging.getLogger(__name__)


def validate_public_url(url):
    """Refuse URLs that could reach the server's own network: https only, no embedded credentials,
    and every address the host resolves to must be public (blocks localhost, Docker networks,
    cloud metadata, RFC 1918). WEBHOOK_ALLOW_INSECURE lifts this for development."""
    insecure = settings.WEBHOOK_ALLOW_INSECURE
    try:
        parts = urlsplit(url)
        port = parts.port or (443 if parts.scheme == 'https' else 80)
    except ValueError:
        raise ValidationError('Invalid URL.')
    if parts.scheme not in (('https', 'http') if insecure else ('https',)):
        raise ValidationError('Webhook URLs must use https.')
    if not parts.hostname:
        raise ValidationError('Invalid URL.')
    if parts.username or parts.password:
        raise ValidationError('Put credentials in the secret, not the URL.')
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(parts.hostname, port, proto=socket.IPPROTO_TCP)}
    except (socket.gaierror, UnicodeError):
        raise ValidationError(f'Could not resolve "{parts.hostname}".')
    if not insecure and not all(ipaddress.ip_address(address).is_global for address in addresses):
        raise ValidationError('Webhook URLs may not point at private or internal addresses.')


def build_payload(submission, event, action=None, user=None):
    # Deliberately thin: receivers fetch anything else from `url` with their own credentials.
    return {
        'event': event,
        'action': action,
        'id': submission.id,
        'internal_id': submission.internal_id,
        'lab': submission.lab.lab_id,
        'type': {'id': submission.type_id, 'name': submission.type.name},
        'status': submission.status,
        'actor': user.username if user and user.is_authenticated else None,  # lets API clients ignore their own changes
        'timestamp': timezone.now().isoformat(),
        'url': f'{get_lab_uri(submission.lab)}{get_script_prefix()}api/submissions/{submission.id}/',
        'html_url': submission.get_absolute_url(full_url=True),
    }


def notify(submission, event, action=None, user=None):
    """Send `event` to the submission's webhook, if it has one, once the current transaction commits."""
    webhook = Webhook.for_submission(submission)
    if webhook:
        payload = build_payload(submission, event, action, user)
        transaction.on_commit(lambda: send(webhook, payload))


def send(webhook, payload):
    if not settings.WEBHOOK_ASYNC:
        return deliver(webhook, payload)
    def run():
        try:
            deliver(webhook, payload)
        finally:
            connection.close()  # this thread's own DB connection
    threading.Thread(target=run, daemon=True).start()


def deliver(webhook, payload):
    """POST `payload` and record the outcome on the webhook. Returns (status_code, error)."""
    status, error = None, ''
    try:
        validate_public_url(webhook.url)  # again at send time: DNS may have changed since it was saved
        headers = {'User-Agent': 'CoreOmics-Webhook/1', 'X-CoreOmics-Event': payload['event'], 'X-CoreOmics-Delivery': str(uuid.uuid4())}
        if webhook.encrypted_secret:
            headers[webhook.auth_header] = webhook.secret
        # stream=True: only the status line is read, never the (possibly huge) response body.
        with requests.post(webhook.url, json=payload, headers=headers, timeout=settings.WEBHOOK_TIMEOUT, allow_redirects=False, stream=True) as response:
            status = response.status_code
        if status >= 300:
            error = f'HTTP {status}'
    except Exception as e:
        # Record only the exception type: request errors can echo the URL (and its query string).
        error = e.messages[0] if isinstance(e, ValidationError) else type(e).__name__
    if error:
        logger.warning('Webhook %s delivery failed: %s', webhook.pk, error)
    Webhook.objects.filter(pk=webhook.pk).update(last_sent=timezone.now(), last_status=status, last_error=error[:250])
    return status, error
