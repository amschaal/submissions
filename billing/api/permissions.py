from rest_framework import permissions
from dnaorder.models import Submission


class LineItemPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action not in ['create','list']:
            return True
        id = request.query_params.get('submission') if request.method == 'GET' else request.data.get('submission')
        submission = Submission.objects.filter(id=id).first()
        if not submission:
            return False
        perms = submission.permissions(request.user)
        return Submission.PERMISSION_ADMIN in perms or Submission.PERMISSION_STAFF in perms
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.editable(request.user)
