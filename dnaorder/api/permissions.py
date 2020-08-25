from rest_framework import permissions

def is_lab_member(lab, user):
    return lab.users.filter(id=user.id).exists()

class SubmissionFilePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.submission.editable(request.user)

class ReadOnlyPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return request.user.is_staff

class SubmissionTypePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return is_lab_member(obj.lab, request.user)

class ProjectIDPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return is_lab_member(obj.lab, request.user)


class NotePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.can_modify(request.user)
    
class SubmissionPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list' and not request.user.is_authenticated:
            return False
#         if request.user.is_authenticated:
#             return True
#         if request.method in permissions.SAFE_METHODS and view.action != 'list': 
#             return True
#         if view.action == 'create': #right now we let people anonymously submit
#             return True
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.editable(request.user)

class IsLabMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(obj, 'submission') and hasattr(obj.submission, 'lab'):
            return is_lab_member(obj.submission.lab, request.user)
        elif hasattr(obj, 'lab'):
            return is_lab_member(obj.lab, request.user)
        return False
            

class DraftPermissions(SubmissionPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
# 
#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user

class IsStaffPermission(permissions.BasePermission):
    """
    The request is authenticated as staff, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsSuperuserPermission(permissions.BasePermission):
    """
    The request is authenticated as a superuser, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )