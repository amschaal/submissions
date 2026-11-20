"""What can be read without signing in: the little the landing pages show.

The site landing page lists the institution's labs and each lab has a landing
page with its own welcome text.  Nothing else about a lab is exposed here: no
submission types, contact addresses, settings, plugins or people.  Keep the
serializers to an explicit list of fields so that nothing added to the model
later becomes public by accident.

(The institution's own name, logo and welcome text come from
``/api/institutions/default/``.)
"""
from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from dnaorder.models import Lab
from dnaorder.utils import get_site_institution


class PublicLabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['lab_id', 'name']
        read_only_fields = fields


class PublicLabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['lab_id', 'name', 'home_page']
        read_only_fields = fields


class PublicLabViewSet(viewsets.ReadOnlyModelViewSet):
    """The current institution's enabled labs, by name, and one lab's landing page."""
    permission_classes = [AllowAny]
    lookup_field = 'lab_id'
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        return Lab.objects.filter(institution=get_site_institution(self.request), disabled=False).order_by('name')

    def get_serializer_class(self):
        return PublicLabSerializer if self.detail else PublicLabListSerializer
