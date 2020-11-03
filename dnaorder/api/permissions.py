from rest_framework import permissions


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
        return obj.lab.is_lab_member(request.user)

class ProjectIDPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # May not modify file unless submission is "editable".
        return obj.lab.is_lab_member(request.user)


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

class ObjectPermission(permissions.BasePermission):
#     permission = None
#     use_superuser = True
#     def __new__(cls, permission, use_superuser=True):
#         print('__new__:', cls, permission, use_superuser)
#         instance = super(ObjectPermission, cls).__new__(cls)
#         print('instance', instance)
#         instance.permission = permission
#         instance.use_superuser = use_superuser
#         return instance
#         cls.permission = permission
#         cls.use_superuser = use_superuser
#         return cls
    @classmethod
    def create(cls, permission, use_superuser=True):
#         return cls.__new__(cls, permission, use_superuser)
        return type('CustomObjectPermission', (cls,), {'permission': permission, 'use_superuser': use_superuser})
#         class foo(cls):
#             permission = permission
#             use_superuser = use_superuser
#         return foo
    def has_object_permission(self, request, view, obj):
#         print('has_object_permission', self.__class__, view, obj, self.permission)
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
        return None

# foo = LabObjectPermission.create('foo')
# bar = LabObjectPermission.create('bar')
# print('foo', foo, foo.permission)
# print('bar', bar, bar.permission)

