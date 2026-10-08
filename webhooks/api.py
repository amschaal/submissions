import logging
import re

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dnaorder.api.filters import LabFilter
from dnaorder.api.permissions import LabAdmin
from dnaorder.models import Lab, LabPermission
from dnaorder.utils import get_site_institution
from webhooks.delivery import deliver, validate_public_url
from webhooks.models import Webhook

logger = logging.getLogger(__name__)
HEADER_NAME = re.compile(r'[A-Za-z0-9-]{1,100}')
RESERVED_HEADERS = {'host', 'connection', 'content-length', 'content-type', 'transfer-encoding'}


class WebhookSerializer(serializers.ModelSerializer):
    # Declared explicitly so DRF doesn't derive a UniqueValidator for `lab` from the conditional
    # constraint (it would also reject per-type overrides); uniqueness is checked in validate().
    lab = serializers.PrimaryKeyRelatedField(queryset=Lab.objects.all())
    secret = serializers.CharField(write_only=True, required=False, allow_blank=True, trim_whitespace=False)  # omit to keep, "" to clear
    has_secret = serializers.SerializerMethodField()

    class Meta:
        model = Webhook
        fields = ['id', 'lab', 'submission_type', 'enabled', 'url', 'auth_header', 'secret', 'has_secret', 'last_sent', 'last_status', 'last_error']

    def get_has_secret(self, webhook):
        return bool(webhook.encrypted_secret)

    def validate_url(self, url):
        if url:
            validate_public_url(url)
        return url

    def validate_auth_header(self, name):
        if not HEADER_NAME.fullmatch(name) or name.lower() in RESERVED_HEADERS:
            raise serializers.ValidationError('Enter a valid HTTP header name, e.g. "Authorization".')
        return name

    def validate_secret(self, secret):
        if secret and not settings.WEBHOOK_ENCRYPTION_KEYS:
            raise serializers.ValidationError('Secrets cannot be stored until WEBHOOK_ENCRYPTION_KEYS is configured on the server.')
        if '\r' in secret or '\n' in secret:
            raise serializers.ValidationError('The secret may not contain line breaks.')
        return secret

    def validate(self, attrs):
        current = self.instance or Webhook()  # model defaults for anything a create omits
        if attrs.get('enabled', current.enabled) and not attrs.get('url', current.url):
            raise serializers.ValidationError({'url': 'A URL is required while the webhook is enabled.'})
        if self.instance:  # lab and submission type are fixed once created
            for field in ('lab', 'submission_type'):
                attrs.pop(field, None)
            return attrs
        lab, submission_type = attrs['lab'], attrs.get('submission_type')
        if submission_type and submission_type.lab_id != lab.id:
            raise serializers.ValidationError({'submission_type': 'Must belong to the same lab.'})
        if Webhook.objects.filter(lab=lab, submission_type=submission_type).exists():
            raise serializers.ValidationError('This lab or submission type already has a webhook.')
        return attrs


class WebhookViewSet(viewsets.ModelViewSet):
    """Lab admins manage their labs' webhooks. Secrets are write-only and encrypted at rest;
    `reveal_secret` is the only way to read one back."""
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated, LabAdmin]
    filter_backends = viewsets.ModelViewSet.filter_backends + [LabFilter]
    filterset_fields = {'submission_type': ['exact', 'isnull']}
    lab_filter = 'lab__lab_id'
    pagination_class = None

    def get_queryset(self):
        queryset = Webhook.objects.filter(lab__institution=get_site_institution(self.request)).select_related('lab', 'submission_type')
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(lab__permissions__user=self.request.user, lab__permissions__permission=LabPermission.PERMISSION_ADMIN)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data['lab'])
        serializer.save()

    @action(detail=True, methods=['post'])
    def reveal_secret(self, request, pk=None):
        webhook = self.get_object()
        logger.warning('Webhook %s secret revealed to user "%s"', webhook.pk, request.user.username)
        return Response({'secret': webhook.secret}, headers={'Cache-Control': 'no-store'})

    @action(detail=True, methods=['post'])
    def ping(self, request, pk=None):
        webhook = self.get_object()
        status, error = deliver(webhook, {'event': 'ping', 'webhook': webhook.id, 'actor': request.user.username, 'timestamp': timezone.now().isoformat()})
        return Response({'status': status, 'error': error})
