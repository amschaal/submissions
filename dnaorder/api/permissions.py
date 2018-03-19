from rest_framework import permissions

class SubmissionFilePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.submission.editable(request.user)