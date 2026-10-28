from django.conf import settings
from django.db import transaction
from django.http import FileResponse, Http404
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.reverse import reverse

from dnaorder.api.filters import LabFilter
from dnaorder.models import Lab, LabFile
from dnaorder.storage import protected_storage
from dnaorder.utils import get_site_institution


class LabFileSerializer(serializers.ModelSerializer):
    lab = serializers.PrimaryKeyRelatedField(queryset=Lab.objects.all())
    file = serializers.FileField(write_only=True)  # read back through `url`, never the storage path
    filename = serializers.ReadOnlyField()
    size = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')

    class Meta:
        model = LabFile
        fields = ['id', 'lab', 'name', 'description', 'internal', 'file', 'filename', 'size', 'url', 'created', 'modified', 'uploaded_by']

    def get_size(self, lab_file):
        try:
            return lab_file.file.size
        except FileNotFoundError:
            return None

    def get_url(self, lab_file):
        return reverse('lab_files-download', args=[lab_file.pk], request=self.context.get('request'))

    def validate_lab(self, lab):
        request = self.context.get('request')
        if request and lab.institution_id != get_site_institution(request).id:
            raise serializers.ValidationError('Invalid lab.')
        return lab

    def validate_file(self, file):
        if file.size > settings.LAB_FILE_MAX_UPLOAD_MB * 1024 * 1024:
            raise serializers.ValidationError(f'Files may not be larger than {settings.LAB_FILE_MAX_UPLOAD_MB} MB.')
        return file

    def update(self, instance, validated_data):
        validated_data.pop('lab', None)  # a file can't move between labs
        old_name = instance.file.name if 'file' in validated_data else None
        instance = super().update(instance, validated_data)
        if old_name and old_name != instance.file.name:
            transaction.on_commit(lambda: protected_storage.delete(old_name))
        return instance


class LabFilePermissions(permissions.BasePermission):
    """Reads are limited by the queryset; lab admins/members manage the files."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        lab = obj if isinstance(obj, Lab) else obj.lab
        return lab.is_lab_member(request.user)


class LabFileViewSet(viewsets.ModelViewSet):
    """Files labs offer for download, such as form templates. Only lab staff can list them;
    anyone can fetch a public file by id, while internal files 404 for users without a lab permission."""
    serializer_class = LabFileSerializer
    permission_classes = [LabFilePermissions]
    filter_backends = viewsets.ModelViewSet.filter_backends + [LabFilter]
    filterset_fields = {'internal': ['exact']}
    lab_filter = 'lab__lab_id'
    pagination_class = None

    def get_queryset(self):
        user, institution = self.request.user, get_site_institution(self.request)
        queryset = LabFile.objects.for_lab_staff(user, institution) if self.action == 'list' else LabFile.objects.visible_to(user, institution)
        return queryset.select_related('lab', 'uploaded_by')

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data['lab'])
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        lab_file = self.get_object()
        try:
            response = FileResponse(lab_file.file.open('rb'), as_attachment=True, filename=lab_file.filename)
        except FileNotFoundError:
            raise Http404
        if lab_file.internal:
            response['Cache-Control'] = 'private, no-store'
        return response
