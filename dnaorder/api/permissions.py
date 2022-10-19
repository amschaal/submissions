from rest_framework import permissions
from dnaorder.models import LabPermission


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
        if request.method in permissions.SAFE_METHODS or request.user and request.user.is_superuser:
            return True
        # May not modify file unless submission is "editable".
        return obj.lab.permissions.filter(permission__in=[LabPermission.PERMISSION_ADMIN, LabPermission.PERMISSION_MEMBER], user=request.user).exists()
#         return obj.lab.is_lab_member(request.user)

class ProjectIDPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user and request.user.is_superuser:
            return True
        # May not modify file unless submission is "editable".
#         return obj.lab.is_lab_member(request.user)
        return obj.lab.permissions.filter(permission__in=[LabPermission.PERMISSION_ADMIN, LabPermission.PERMISSION_MEMBER], user=request.user).exists()


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
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.editable(request.user)

class IsLabMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        from dnaorder.models import Lab
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if isinstance(obj, Lab):
            return obj.is_lab_member(request.user)
        if hasattr(obj, 'submission') and hasattr(obj.submission, 'lab'):
            return obj.submission.lab.is_lab_member(request.user)
        elif hasattr(obj, 'lab'):
            return obj.lab.is_lab_member(request.user)
        return False
            

class DraftPermissions(SubmissionPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False

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

class ObjectPermission(permissions.BasePermission):
    @classmethod
    def create(cls, permission, use_superuser=True):
        return type(cls.__name__, (cls,), {'permission': permission, 'use_superuser': use_superuser})
    def has_object_permission(self, request, view, obj):
        obj = self.get_obj(obj)
        print(obj.permissions.filter(user=request.user))
        if not obj:
            return False
        if not request.user.is_authenticated:
            return False
        if self.use_superuser and request.user.is_superuser:
            return True
        return obj.permissions.filter(permission=self.permission, user=request.user).exists()
    def get_obj(self, obj):
        return obj # override this if it is a related object, i.e. obj.lab

class LabObjectPermission(ObjectPermission):
    def get_obj(self, obj):
        print('LabObjectPermission.get_obj', obj)
        from dnaorder.models import Lab
        if isinstance(obj, Lab):
            return obj
        if hasattr(obj, 'submission') and hasattr(obj.submission, 'lab') and isinstance(obj.submission.lab, Lab):
            return obj.submission.lab
        elif hasattr(obj, 'lab') and isinstance(obj.lab, Lab):
            return obj.lab
        return None

class InstitutionObjectPermission(ObjectPermission):
    def get_obj(self, obj):
        from dnaorder.models import Institution, Lab
        if isinstance(obj, Institution):
            return obj
        elif isinstance(obj, Lab):
            return obj.institution
        return None

LabAdmin = LabObjectPermission.create(LabPermission.PERMISSION_ADMIN)
LabMember = LabObjectPermission.create(LabPermission.PERMISSION_MEMBER)


