from rest_framework.response import Response
from dnaorder.api.serializers import UserListSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from dnaorder.api.permissions import IsSuperuserPermission

class PermissionMixin(object):
    permission_model = None # Must override this
    manage_permissions_classes = [IsSuperuserPermission]
    def serialize_permissions(self, obj):
        user_perms = {}
        for p in  self.permission_model.objects.filter(permission_object=obj).order_by('user'):
            if p.user.username not in user_perms:
                user_perms[p.user.username] = UserListSerializer(p.user).data
                user_perms[p.user.username]['permissions'] = []
            user_perms[p.user.username]['permissions'].append(p.permission)
        return user_perms
    @action(detail=True, methods=['get'], permission_classes=manage_permissions_classes)
    def permissions(self, request, **kwargs):
#         institution = get_site_institution(request)
        obj = self.get_object()
        user_perms = self.serialize_permissions(obj)
#         serializer = self.permission_modelSerializer(qs, many=True)
        return Response({'available_permissions': self.permission_model.PERMISSION_CHOICES, 'user_permissions': user_perms})
    @action(detail=True, methods=['post'], permission_classes=manage_permissions_classes)
    def set_permissions(self, request, **kwargs):
        obj = self.get_object()
        for username, data in request.data.get('user_permissions').items():
            user = User.objects.get(username=username)
            self.permission_model.objects.filter(permission_object=obj, user=user).delete()
            for p in data.get('permissions', []):
                if p in [choice[0] for choice in self.permission_model.PERMISSION_CHOICES]:
                    self.permission_model.objects.get_or_create(user=user, permission_object=obj, permission=p)
#         self.permission_model.objects.filter(institution=obj).delete()
        user_perms = self.serialize_permissions(obj)
        return Response({'available_permissions': self.permission_model.PERMISSION_CHOICES, 'user_permissions': user_perms})