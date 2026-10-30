from cryptography.fernet import Fernet, MultiFernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import Q

from dnaorder.models import Lab, SubmissionType


def fernet():
    # First key encrypts; every key decrypts, so keys can be rotated by prepending a new one.
    if not settings.WEBHOOK_ENCRYPTION_KEYS:
        raise ImproperlyConfigured('WEBHOOK_ENCRYPTION_KEYS must be set to store webhook secrets.')
    return MultiFernet([Fernet(key) for key in settings.WEBHOOK_ENCRYPTION_KEYS])


class Webhook(models.Model):
    """POSTs a small JSON event to `url` whenever a submission is created or updated.

    A lab has at most one default webhook (submission_type=None); a submission type may
    override it with its own, and a disabled override turns webhooks off for that type.
    """
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='webhooks')
    submission_type = models.OneToOneField(SubmissionType, null=True, blank=True, on_delete=models.CASCADE, related_name='webhook')
    enabled = models.BooleanField(default=True)
    url = models.URLField(max_length=500, blank=True)
    auth_header = models.CharField(max_length=100, default='Authorization')
    encrypted_secret = models.TextField(blank=True, editable=False)  # Fernet token; never serialize
    last_sent = models.DateTimeField(null=True, editable=False)
    last_status = models.IntegerField(null=True, editable=False)
    last_error = models.CharField(max_length=250, blank=True, editable=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['lab'], condition=Q(submission_type=None), name='webhook_one_default_per_lab')]

    def __str__(self):
        return f'{self.lab} / {self.submission_type or "default"}: {self.url}'

    @property
    def secret(self):
        return fernet().decrypt(self.encrypted_secret.encode()).decode() if self.encrypted_secret else ''

    @secret.setter
    def secret(self, value):
        self.encrypted_secret = fernet().encrypt(value.encode()).decode() if value else ''

    @classmethod
    def for_submission(cls, submission):
        """The type's override if it has one, else the lab default; None unless enabled with a URL."""
        hook = cls.objects.filter(submission_type_id=submission.type_id).first() \
            or cls.objects.filter(lab_id=submission.lab_id, submission_type=None).first()
        return hook if hook and hook.enabled and hook.url else None
