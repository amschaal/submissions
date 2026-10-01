from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from dnaorder.models import LabPermission, InstitutionPermission
import sys

from dnaorder.utils import get_site_institution

INTERNAL_TYPE_MESSAGE = 'Only lab members may create or update submissions of an internal submission type.'

class SubmissionFilePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            from dnaorder.models import Submission
            # Files may only be attached to an internal submission by lab members.
            submission = Submission.objects.select_related('type__lab').filter(pk=request.data.get('submission')).first()
            if submission and not submission.type.can_submit(request.user):
                raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        return True
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
        return False #request.user.is_staff

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
    def get_submission_type(self, type):
        from dnaorder.models import SubmissionType
        # The submitted type may be an id or a nested object, depending on the serializer.
        if isinstance(type, dict):
            type = type.get('id')
        if not type:
            return None
        try:
            return SubmissionType.objects.select_related('lab').filter(pk=type).first()
        except (ValueError, TypeError): # e.g. a non numeric id, let the serializer report it
            return None
    def has_permission(self, request, view):
        if view.action == 'list' and not request.user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            # Block non lab members from submitting against an internal type.
            data = request.data if hasattr(request.data, 'get') else {}
            type = self.get_submission_type(data.get('type'))
            if type and not type.can_submit(request.user):
                raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Submissions of an internal type may only be modified by lab members.
        if not obj.type.can_submit(request.user):
            raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        # May not modify file unless submission is "editable".
        return obj.editable(request.user)

class IsLabMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        from dnaorder.models import Lab
        # if request.method in permissions.SAFE_METHODS:
        #     return True
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
            # request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsSuperuserPermission(permissions.BasePermission):
    """
    The request is authenticated as a superuser, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            # request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )

class ObjectPermission(permissions.BasePermission):
    @classmethod
    def create(cls, permission, use_superuser=True):
        return type(cls.__name__, (cls,), {'permission': permission, 'use_superuser': use_superuser})
    # def has_permission(self, request, view): 
    #     if view.detail:
    #         view.get_object() # if this isn't called from the viewset, has_object_permission is not called.  However, if it is and this is run, code is run twice.
    #     return super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        obj = self.get_obj(obj)
        sys.stderr.write('has_object_permission\n')
        # sys.stderr.writelines([str(obj.permissions.filter(user=request.user)),self.permission])
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
        else:
            return get_site_institution(self.request)

# Merely used for testing at this point
class DenyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False

class SubmissionVersionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(username=request.user.username).exists() or request.user.is_superuser
    
class SubmissionTypeVersionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.lab.permissions.filter(permission__in=[LabPermission.PERMISSION_ADMIN, LabPermission.PERMISSION_MEMBER], user=request.user).exists() or request.user.is_superuser)

LabAdmin = LabObjectPermission.create(LabPermission.PERMISSION_ADMIN)
LabMember = LabObjectPermission.create(LabPermission.PERMISSION_MEMBER)

InstitutionAdmin = InstitutionObjectPermission.create(InstitutionPermission.PERMISSION_ADMIN)
