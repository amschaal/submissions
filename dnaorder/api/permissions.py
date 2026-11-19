from django.http import Http404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from dnaorder.models import LabPermission, InstitutionPermission
import sys

from dnaorder.utils import get_site_institution

INTERNAL_TYPE_MESSAGE = 'Only lab members may create or update submissions of an internal submission type.'

LAB_STAFF_ROLES = [LabPermission.PERMISSION_ADMIN, LabPermission.PERMISSION_MEMBER]

class AuthenticatedPermission(permissions.BasePermission):
    """Base for every permission class here: nothing is available without signing in.
    Subclasses that add their own has_permission() must call super() first."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

def visible_submission(request, submission_id):
    """The submission, if the user may open it (Submission.objects.visible_to); otherwise
    404, the same as for an id that does not exist."""
    from dnaorder.models import Submission
    submission = Submission.objects.visible_to(request.user).select_related('type__lab', 'lab').filter(pk=submission_id).first() if submission_id else None
    if not submission:
        raise Http404
    return submission

def is_lab_staff(user, lab_id):
    """Lab ADMIN/MEMBER of the lab with this primary key, or a superuser."""
    if user.is_superuser:
        return True
    try:
        return LabPermission.objects.filter(user=user, permission_object_id=lab_id, permission__in=LAB_STAFF_ROLES).exists()
    except (ValueError, TypeError): # e.g. a non numeric id, let the serializer report it
        return False

class SubmissionFilePermissions(AuthenticatedPermission):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if view.action == 'create' and request.data.get('submission'):
            # (With no submission id the serializer reports the missing field.)
            submission = visible_submission(request, request.data.get('submission'))
            # Files may only be attached to an internal submission by lab members.
            if not submission.type.can_submit(request.user):
                raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.submission.editable(request.user)

class ReadOnlyPermissions(AuthenticatedPermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return False #request.user.is_staff

class SubmissionTypePermissions(AuthenticatedPermission):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if view.action == 'create':
            # Only staff of the lab the new type is created in.
            return is_lab_staff(request.user, request.data.get('lab') if hasattr(request.data, 'get') else None)
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user and request.user.is_superuser:
            return True
        # May not modify file unless submission is "editable".
        return obj.lab.permissions.filter(permission__in=LAB_STAFF_ROLES, user=request.user).exists()
#         return obj.lab.is_lab_member(request.user)

class ProjectIDPermissions(AuthenticatedPermission):
    """Project id prefixes are a lab staff tool: any lab permission to read them (the
    queryset limits which), lab ADMIN/MEMBER to change them."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        user = request.user
        if user.is_superuser:
            return True
        if view.action == 'create':
            return is_lab_staff(user, request.data.get('lab') if hasattr(request.data, 'get') else None)
        return LabPermission.objects.filter(user=user).exists()
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user and request.user.is_superuser:
            return True
        # May not modify file unless submission is "editable".
#         return obj.lab.is_lab_member(request.user)
        return obj.lab.permissions.filter(permission__in=LAB_STAFF_ROLES, user=request.user).exists()


class NotePermissions(AuthenticatedPermission):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if view.action == 'create':
            visible_submission(request, request.data.get('submission') if hasattr(request.data, 'get') else None)
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.can_modify(request.user)
    
class SubmissionPermissions(AuthenticatedPermission):
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
        if not super().has_permission(request, view):
            return False
        if request.method not in permissions.SAFE_METHODS:
            # Block non lab members from submitting against an internal type.
            data = request.data if hasattr(request.data, 'get') else {}
            type = self.get_submission_type(data.get('type'))
            if type and not type.can_submit(request.user):
                raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        return True
    def has_object_permission(self, request, view, obj):
        # Which submissions a user can reach at all is decided by the viewset's
        # queryset (Submission.objects.visible_to); this is about changing one.
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == 'destroy':
            # Deleting is for the lab's administrators; everyone else cancels.
            return request.user.is_superuser or obj.lab.has_permission(request.user, LabPermission.PERMISSION_ADMIN)
        # Submissions of an internal type may only be modified by lab members.
        if not obj.type.can_submit(request.user):
            raise PermissionDenied(INTERNAL_TYPE_MESSAGE)
        # May not modify file unless submission is "editable".
        return obj.editable(request.user)

class IsLabMember(AuthenticatedPermission):
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
            

class DraftPermissions(AuthenticatedPermission):
    """A draft belongs to whoever saved it.  Its link also works for the people it
    names (submitter, PI, contacts), so a draft can be handed to a colleague, and
    for staff helping with it."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser or obj.owner_id == user.pk or obj.names(user):
            return True
        raise Http404 # the same as a draft that does not exist

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

class ObjectPermission(AuthenticatedPermission):
    @classmethod
    def create(cls, permission, use_superuser=True):
        return type(cls.__name__, (cls,), {'permission': permission, 'use_superuser': use_superuser})
    # def has_permission(self, request, view): 
    #     if view.detail:
    #         view.get_object() # if this isn't called from the viewset, has_object_permission is not called.  However, if it is and this is run, code is run twice.
    #     return super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        obj = self.get_obj(obj)
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
class DenyPermission(AuthenticatedPermission):
    def has_object_permission(self, request, view, obj):
        return False

class SubmissionVersionPermission(AuthenticatedPermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(username=request.user.username).exists() or request.user.is_superuser
    
class SubmissionTypeVersionPermission(AuthenticatedPermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.lab.permissions.filter(permission__in=[LabPermission.PERMISSION_ADMIN, LabPermission.PERMISSION_MEMBER], user=request.user).exists() or request.user.is_superuser)

LabAdmin = LabObjectPermission.create(LabPermission.PERMISSION_ADMIN)
LabMember = LabObjectPermission.create(LabPermission.PERMISSION_MEMBER)

InstitutionAdmin = InstitutionObjectPermission.create(InstitutionPermission.PERMISSION_ADMIN)
