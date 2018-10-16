from rest_framework import viewsets, response
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer, NoteSerializer, SubmissionTypeSerializer,\
    UserSerializer
from dnaorder.models import Submission, SubmissionFile, SubmissionStatus, Note,\
    SubmissionType
from rest_framework.decorators import detail_route, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from dnaorder.api.permissions import SubmissionFilePermissions,\
    ReadOnlyPermissions, SubmissionPermissions
from django.core.mail import send_mail
from dnaorder import emails
from dnaorder.views import submission
from dnaorder.validators import SamplesheetValidator, VALIDATORS_DICT,\
    VALIDATORS
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.select_related('type','status').all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'internal_id':['icontains','exact'],'phone':['icontains'],'name':['icontains'],'email':['icontains'],'pi_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status__name':['icontains'],'biocore':['exact'],'locked':['exact'],'type':['exact']}
    search_fields = ('id', 'internal_id', 'institute', 'name', 'notes', 'email', 'pi_email', 'pi_name', 'type__name')
    ordering_fields = ['id','internal_id', 'phone','name','email','pi_name','pi_email','institute','type__name','submitted','status__order','biocore','locked']
    permission_classes = [SubmissionPermissions]
    @detail_route(methods=['post'])
    def update_status(self,request,pk):
        submission = self.get_object()
        status = SubmissionStatus.objects.get(id=request.data.get('status'))
        submission.set_status(status,commit=True)
        text = 'Submission status updated to "{status}".'.format(status=submission.status.name)
        if request.data.get('email',False):
#             emails.status_update(submission,request=request)
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,emails=[submission.email],public=True)
            return response.Response({'status':'success','locked':submission.locked,'message':'Status updated. Email sent to "{0}".'.format(submission.email)})
        else:
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,public=True)
        return response.Response({'status':'success','locked':submission.locked,'message':'Status updated.'})
    @detail_route(methods=['post'])
    def lock(self,request,pk):
        submission = self.get_object()
        submission.locked = True
        submission.save()
        return response.Response({'status':'success','locked':True,'message':'Submission locked.'})
    @detail_route(methods=['post'])
    def unlock(self,request,pk):
        submission = self.get_object()
        submission.locked = False
        submission.save()
        return response.Response({'status':'success','locked':False,'message':'Submission unlocked.'})

class SubmissionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubmissionType.objects.all().annotate(submission_count=Count('submissions')).order_by('id')
    serializer_class =SubmissionTypeSerializer
    permission_classes = [ReadOnlyPermissions]
    permission_classes_by_action = {'validate_data': [AllowAny]}
    search_fields = ('name', 'description')
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
#     @detail_route(methods=['post'])
#     def show(self,request,pk):
#         submission_type = self.get_object()
#         SubmissionType.objects.filter(original=submission_type.original).update(show=False)
#         submission_type.show = True
#         submission_type.save()
#         return response.Response({'status':'success','message':'Version {0} set to default.'.format(submission_type.version)})
    @detail_route(methods=['post'])
    def validate_data(self,request, pk):
        submission_type = self.get_object()
        validator = SamplesheetValidator(submission_type.schema,request.data.get('data'))
        errors = validator.validate() #validate_samplesheet(submission_type.schema,request.data.get('data'))
        if len(errors) == 0:
            return response.Response({'status':'success','message':'The data was succussfully validated'})
        else:
            return response.Response({'errors':errors},status=500)
    

class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer
    filter_fields = {'submission':['exact']}
    permission_classes = [SubmissionFilePermissions]
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        submission = self.request.query_params.get('submission',None)
        if self.request.user.is_authenticated:
            return queryset
        else:
            if not submission:
                raise PermissionDenied('Unauthenticated users must provide a submission id in the request.')
            return queryset.filter(submission=submission)
#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [SubmissionFilePermissions]
#         return [permission() for permission in permission_classes]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.submission.editable(request.user):
            raise PermissionDenied('Only authenticated users may delete files once a submission is final.')
        return super(SubmissionFileViewSet, self).destroy(request,*args,**kwargs)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_fields = {'submission':['exact']}
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        submission = self.request.query_params.get('submission',None)
        if self.request.user.is_authenticated:
            return queryset
        else:
            if not submission:
                raise PermissionDenied('Unauthenticated users must provide a submission id in the request.')
            return queryset.filter(submission=submission,public=True)
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# 
#     def perform_create(self, serializer):
#         serializer.save()
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    ordering_fields = ['name','first_name','last_name']
    permission_classes = (IsAuthenticated,)

class ValidatorViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        VALIDATORS_DICT.get(pk)
    def list(self, request):
        return response.Response([v().serialize() for v in VALIDATORS])
