from rest_framework import viewsets, response, status
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer, NoteSerializer, SubmissionTypeSerializer,\
    UserSerializer, StatusSerializer, WritableSubmissionSerializer,\
    DraftSerializer, LabSerializer, PrefixSerializer, VocabularySerializer,\
    TermSerializer, ImportSubmissionSerializer, ImportSerializer
from dnaorder.models import Submission, SubmissionFile, SubmissionStatus, Note,\
    SubmissionType, Draft, Lab, PrefixID, Vocabulary, Term, Import
from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny,\
    IsAuthenticatedOrReadOnly
from dnaorder.api.permissions import SubmissionFilePermissions,\
    ReadOnlyPermissions, SubmissionPermissions, DraftPermissions
from django.core.mail import send_mail
from dnaorder import emails
# from dnaorder.views import submission
from dnaorder.validators import SamplesheetValidator, VALIDATORS_DICT,\
    VALIDATORS
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from dnaorder.utils import get_site_lab
from dnaorder.api.filters import ParticipatingFilter, ExcludeStatusFilter
from dnaorder.import_utils import import_submission_url

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related('type').all()
    serializer_class = SubmissionSerializer
    filter_backends = viewsets.ModelViewSet.filter_backends + [ParticipatingFilter, ExcludeStatusFilter]
    filter_fields = {'id':['icontains','exact'],'internal_id':['icontains','exact'],'import_internal_id':['icontains','exact'],'phone':['icontains'],'first_name':['icontains'],'last_name':['icontains'],'email':['icontains'],'pi_first_name':['icontains'],'pi_last_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status':['icontains','iexact'],'biocore':['exact'],'locked':['exact'],'type':['exact'],'cancelled':['isnull']}
    search_fields = ('id', 'internal_id', 'import_internal_id', 'institute', 'first_name', 'last_name', 'notes', 'email', 'pi_email', 'pi_first_name','pi_last_name','pi_phone', 'type__name', 'status')
    ordering_fields = ['id','internal_id', 'import_internal_id', 'phone','first_name', 'last_name', 'email','pi_first_name', 'pi_last_name','pi_email','pi_phone','institute','type__name','submitted','status','biocore','locked']
    permission_classes = [SubmissionPermissions]
    permission_classes_by_action = {'cancel': [AllowAny]}
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self).select_related('lab')
        lab = get_site_lab(self.request)
        return queryset.filter(lab=lab)
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return WritableSubmissionSerializer
        return SubmissionSerializer
#         return viewsets.ModelViewSet.get_serializer_class(self)
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
#     @action(detail=False, methods=['post','get'])
#     def import_submission(self, request):
#         url = request.query_params.get('url')
#         type = int(request.query_params.get('type'))
#         data = import_submission_url(url)
# #         data['type'] =  data['type']['id']
# #         del data['id']
#         submission = ImportSubmissionSerializer(data=data, type=type)
#         if submission.is_valid():
#             pass # submission.save()
#         return Response({'submission':data, 'errors': submission.errors})
    @action(detail=True, methods=['post'])
    def update_status(self,request,pk):
        submission = self.get_object()
#         status = SubmissionStatus.objects.get(id=request.data.get('status'))
#         submission.set_status(status,commit=True)
        status = request.data.get('status', None)
        submission.status = status
        submission.save()
        text = 'Submission status updated to "{status}".'.format(status=status)
        if request.data.get('email',False):
#             emails.status_update(submission,request=request)
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,emails=[submission.email],public=True)
            return response.Response({'status':'success','locked':submission.locked,'message':'Status updated. Email sent to "{0}".'.format(submission.email)})
        else:
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,public=True)
        return response.Response({'status':'success','locked':submission.locked,'message':'Status updated.'})
    @action(detail=True, methods=['post'])
    def lock(self,request,pk):
        submission = self.get_object()
        submission.locked = True
        submission.save()
        return response.Response({'status':'success','locked':True,'message':'Submission locked.'})
    @action(detail=True, methods=['post'])
    def unlock(self,request,pk):
        submission = self.get_object()
        submission.locked = False
        submission.save()
        return response.Response({'status':'success','locked':False,'message':'Submission unlocked.'})
    @action(detail=True, methods=['post'])
    def cancel(self,request,pk):
        submission = self.get_object()
        if submission.locked and not request.user.is_staff:
            return response.Response({'status':'error', 'message': 'Only staff may cancel a locked submission.'},status=403)
        if not submission.cancelled:
            submission.cancel()
        return response.Response({'status':'success','cancelled':True,'message':'Submission cancelled.'})
    @action(detail=True, methods=['post'])
    def uncancel(self,request,pk):
        submission = self.get_object()
        if not request.user.is_staff:
            return response.Response({'status':'error', 'message': 'Only staff may "uncancel" a submission.'},status=403)
        submission.cancelled = None
        submission.save()
        return response.Response({'status':'success','cancelled':True,'message':'Submission "uncancelled".'})
    @action(detail=True, methods=['post'])
    def confirm(self,request,pk):
        submission = self.get_object()
        if not submission.confirmed:
            submission.confirmed = timezone.now()
            submission.save()
            emails.order_confirmed(submission, request)
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    def perform_create(self, serializer):
        instance = serializer.save(lab=get_site_lab(self.request))
        emails.order_confirmed(instance, self.request)
#         emails.confirm_order(instance, self.request)
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         data = serializer.data
#         del data['id'] #Hide this so that they have to check their email to confirm
#         return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class ImportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Import.objects.all().prefetch_related('submissions')
    serializer_class = ImportSerializer
    filter_fields = {'submissions__id': ['isnull']}
#     search_fields = ('id', 'internal_id', 'institute', 'first_name', 'last_name', 'notes', 'email', 'pi_email', 'pi_first_name','pi_last_name','pi_phone', 'type__name', 'status')
    ordering_fields = ['created']
#     permission_classes = [SubmissionPermissions]
    @action(detail=False, methods=['post','get'])
    def import_submission(self, request):
        url = request.query_params.get('url')
        data = import_submission_url(url)
        instance = Import.objects.create(url=data['url'],api_url=url,data=data)
        serializer = ImportSerializer(instance)
        return Response({'data':data, 'import': serializer.data})
    @action(detail=False, methods=['get'])
    def get_submission(self, request):
        url = request.query_params.get('url')
        data = import_submission_url(url)
        return Response({'data':data})

class SubmissionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubmissionType.objects.all().annotate(submission_count=Count('submissions')).order_by('sort_order', 'name')
    serializer_class = SubmissionTypeSerializer
    permission_classes = [ReadOnlyPermissions]
    permission_classes_by_action = {'validate_data': [AllowAny]}
    search_fields = ('name', 'description')
    filter_fields = {'active':['exact']}
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        lab = get_site_lab(self.request)
        return queryset.filter(lab=lab)
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
    def perform_create(self, serializer):
        return serializer.save(lab=get_site_lab(self.request))
#     @detail_route(methods=['post'])
#     def validate_data(self,request, pk):
#         submission_type = self.get_object()
#         validator = SamplesheetValidator(submission_type.sample_schema,request.data.get('data'))
#         errors = validator.validate() #validate_samplesheet(submission_type.schema,request.data.get('data'))
#         if len(errors) == 0:
#             return response.Response({'status':'success','message':'The data was succussfully validated'})
#         else:
#             return response.Response({'errors':errors},status=500)
    

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

class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubmissionStatus.objects.all().order_by('order')
    serializer_class = StatusSerializer
    ordering_fields = ['order']
    permission_classes = (AllowAny,)

class ValidatorViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        VALIDATORS_DICT.get(pk)
    def list(self, request):
        return response.Response([v().serialize() for v in VALIDATORS])

class DraftViewSet(viewsets.ModelViewSet):
    queryset = Draft.objects.all().order_by('-updated')
    serializer_class = DraftSerializer
    permission_classes = (DraftPermissions,)

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @action(detail=False, methods=['get'])
    def default(self, request):
        lab = get_site_lab(request)
        serializer = self.get_serializer(lab, many=False)
        return Response(serializer.data)

class PrefixViewSet(viewsets.ModelViewSet):
    queryset = PrefixID.objects.all()
    serializer_class = PrefixSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = {'lab_id':['exact']}
#     def get_queryset(self):
#         queryset = viewsets.ModelViewSet.get_queryset(self)
#         lab = get_site_lab(self.request)
#         return queryset.filter(lab=lab)   

class VocabularyViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Vocabulary.objects.distinct()
    serializer_class = VocabularySerializer
    search_fields = ['id', 'name']
    filter_fields = {
        'name':['icontains','exact'],
        'id':['icontains','exact']
        }

class TermViewSet(viewsets.ReadOnlyModelViewSet):
    filter_fields = {
        'value':['icontains','exact']
#         'barcodes':['icontains','exact']
        }
    search_fields = ['value']
    serializer_class = TermSerializer
    queryset = Term.objects.distinct()
    lookup_field = 'value'
    def get_queryset(self):
        return viewsets.ReadOnlyModelViewSet.get_queryset(self).filter(vocabulary=self.kwargs.get('vocabulary'))
    def get_object(self):
        return viewsets.ReadOnlyModelViewSet.get_object(self)