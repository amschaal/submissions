from rest_framework import viewsets, response, status, mixins
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer, NoteSerializer, SubmissionTypeSerializer,\
    UserSerializer, WritableSubmissionSerializer,\
    DraftSerializer, LabSerializer,  VocabularySerializer,\
    TermSerializer, ImportSubmissionSerializer, ImportSerializer,\
    ListSubmissionSerializer, InstitutionSerializer, LabListSerializer,\
    WritableUserSerializer, ProjectIDSerializer, UserListSerializer,\
    InstitutionPermissionSerializer
from dnaorder.models import Submission, SubmissionFile, Note,\
    SubmissionType, Draft, Lab, Vocabulary, Term, Import, UserProfile,\
    Institution, UserEmail, ProjectID, InstitutionPermission, LabPermission
from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from dnaorder.api.permissions import SubmissionFilePermissions,\
    ReadOnlyPermissions, SubmissionPermissions, DraftPermissions,\
    IsStaffPermission, IsSuperuserPermission, NotePermissions,\
    SubmissionTypePermissions, ProjectIDPermissions, IsLabMember,\
    LabObjectPermission, InstitutionObjectPermission
from django.core.mail import send_mail
from dnaorder import emails
# from dnaorder.views import submission
from dnaorder.validators import SamplesheetValidator, VALIDATORS_DICT,\
    VALIDATORS
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.utils import timezone
from rest_framework.response import Response
from dnaorder.utils import get_site_institution
from dnaorder.api.filters import ParticipatingFilter, ExcludeStatusFilter,\
    LabFilter, MySubmissionsFilter, UserFilter
from dnaorder.import_utils import import_submission_url, export_submission,\
    get_submission_schema
from django.conf import settings
import uuid
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from dnaorder.emails import claim_email
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.authtoken.models import Token
from dnaorder.api.mixins import PermissionMixin

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related('type').all()
    serializer_class = SubmissionSerializer
    filter_backends = viewsets.ModelViewSet.filter_backends + [ParticipatingFilter, MySubmissionsFilter, ExcludeStatusFilter, LabFilter]
    filter_fields = {'id':['icontains','exact'],'internal_id':['icontains','exact'],'import_internal_id':['icontains','exact'],'phone':['icontains'],'first_name':['icontains'],'last_name':['icontains'],'email':['icontains'],'pi_first_name':['icontains'],'pi_last_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status':['icontains','iexact'],'biocore':['exact'],'locked':['exact'],'type':['exact'],'cancelled':['isnull']}
    search_fields = ('id', 'internal_id', 'import_internal_id', 'institute', 'first_name', 'last_name', 'notes', 'email', 'pi_email', 'pi_first_name','pi_last_name','pi_phone', 'type__name', 'status')
    lab_filter = 'lab__lab_id'
    ordering_fields = ['id','internal_id', 'import_internal_id', 'phone','first_name', 'last_name', 'email','pi_first_name', 'pi_last_name','pi_email','pi_phone','institute','type__name','submitted','status','biocore','locked']
    permission_classes = [SubmissionPermissions]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes_by_action = {'cancel': [AllowAny]}
    def get_queryset(self):
        if self.detail:
            return Submission.objects.all().select_related('lab')
        institution = get_site_institution(self.request)
        return Submission.get_queryset(institution=institution, user=self.request.user)
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return WritableSubmissionSerializer
        return SubmissionSerializer if self.detail else ListSubmissionSerializer
#         return viewsets.ModelViewSet.get_serializer_class(self)
#     def get_permissions(self):
#         try:
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             return [permission() for permission in self.permission_classes]
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             return self.get_paginated_response([self.get_serializer(s).data for s in page])
#         return Response([self.get_serializer(s).data for s in queryset])
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
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember], authentication_classes=[SessionAuthentication])
    def update_participants(self,request, pk):
        submission = self.get_object()
        participants = [p if isinstance(p, int) else p['id'] for p in request.data.get('participants', [])]
        submission.participants.set(participants)
#         submission.save()
        return response.Response({'status':'success', 'message':'Participants updated.'})
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember])
    def update_status(self,request,pk):
        submission = self.get_object()
#         status = SubmissionStatus.objects.get(id=request.data.get('status'))
#         submission.set_status(status,commit=True)
        status = request.data.get('status', None)
        submission.status = status
        if status.strip().lower() == 'samples received' and not submission.samples_received:
            submission.samples_received = str(timezone.now())[:10]
            submission.received_by = request.user
        submission.save()
        text = 'Submission status updated to "{status}".'.format(status=status)
        if request.data.get('email',False):
#             emails.status_update(submission,request=request)
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,emails=[submission.email],public=True)
            return response.Response({'status':'success','locked':submission.locked,'message':'Status updated. Email sent to "{0}".'.format(submission.email)})
        else:
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,public=True)
        return response.Response({'status':'success','locked':submission.locked,'message':'Status updated.'})
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember], authentication_classes=[SessionAuthentication])
    def update_id(self, request, pk):
        submission = self.get_object()
        project_id = request.data.get('project_id', None)
        project_id = ProjectID.objects.get(id=project_id, lab=submission.lab)
        submission.internal_id = project_id.generate_id(True, True)
        submission.save()
        text = 'Assigned new submission ID "{}".'.format(submission.internal_id)
        if request.data.get('email',False):
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,emails=[submission.email],public=True)
            return response.Response({'status':'success','internal_id':submission.internal_id,'message':'ID updated. Email sent to "{0}".'.format(submission.email)})
        else:
            Note.objects.create(submission=submission,text=text,type=Note.TYPE_LOG,created_by=request.user,public=True)
        return response.Response({'status':'success','internal_id':submission.internal_id,'message':'ID updated.'})
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember], authentication_classes=[SessionAuthentication])
    def lock(self, request, pk):
        submission = self.get_object()
        submission.locked = True
        submission.save()
        return response.Response({'status':'success','locked':True,'message':'Submission locked.'})
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember], authentication_classes=[SessionAuthentication])
    def unlock(self, request, pk):
        submission = self.get_object()
        submission.locked = False
        submission.save()
        return response.Response({'status':'success','locked':False,'message':'Submission unlocked.'})
    @action(detail=True, methods=['post'], permission_classes=[AllowAny], authentication_classes=[SessionAuthentication])
    def cancel(self, request, pk):
        submission = self.get_object()
        if submission.locked and not submission.lab.is_lab_member(request.user):
            return response.Response({'status':'error', 'message': 'Only staff may cancel a locked submission.'},status=403)
        if not submission.cancelled:
            submission.cancel()
        return response.Response({'status':'success','cancelled':True,'message':'Submission cancelled.'})
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember], authentication_classes=[SessionAuthentication])
    def uncancel(self, request, pk):
        submission = self.get_object()
        if not request.user.is_staff:
            return response.Response({'status':'error', 'message': 'Only staff may "uncancel" a submission.'},status=403)
        submission.cancelled = None
        submission.save()
        return response.Response({'status':'success','cancelled':True,'message':'Submission "uncancelled".'})
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def confirm(self, request, pk):
        submission = self.get_object()
        if not submission.confirmed:
            submission.confirmed = timezone.now()
            submission.save()
            emails.order_confirmed(submission, request)
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    @action(detail=True, methods=['post'], permission_classes=[IsLabMember])
    def samples_received(self, request, pk):
#         if not request.user.is_staff:
#             return response.Response({'status':'error', 'message': 'Only staff may set samples as received.'},status=403)
        submission = self.get_object()
        received = request.data.get('received')
        if not received:
            received = timezone.now()
        submission.samples_received = str(received)[:10]
        submission.received_by = User.objects.get(id=request.data.get('received_by', request.user.id))
        submission.save()
        serializer = SubmissionSerializer(submission, context=self.get_serializer_context())
#         serializer = self.get_serializer(submission)
        return Response({'submission':serializer.data})
    def perform_create(self, serializer):
#         instance = serializer.save(lab=get_site_lab(self.request))
        instance = serializer.save()
        emails.order_confirmed(instance, self.request)
        if hasattr(settings, 'BIOCORE_IMPORT_URL') and instance.biocore:
            try:
                export_submission(instance, settings.BIOCORE_IMPORT_URL)
            except Exception as e:
                pass
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
    search_fields = ('submissions__id', 'submissions__internal_id', 'external_id', 'id', 'url')
    ordering_fields = ['created']
    permission_classes = (AllowAny,)
#     permission_classes = [SubmissionPermissions]
    @action(detail=False, methods=['post'])
    def import_submission(self, request):
        url = request.data.get('url')
        data = import_submission_url(url)
        id = data['id']
        instance = Import.objects.filter(id=id).first()
        if not instance:
            instance = Import.objects.create(id=id, url=data['url'], external_id=data['internal_id'], api_url=url,data=data)
        serializer = ImportSerializer(instance)
        return Response({'data':data, 'import': serializer.data})
    @action(detail=False, methods=['get'])
    def get_submission(self, request):
        url = request.query_params.get('url')
        data = import_submission_url(url)
        return Response({'data':data})

class SubmissionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubmissionType.objects.all().annotate(submission_count=Count('submissions')).order_by('sort_order', 'name')
    filter_backends = viewsets.ModelViewSet.filter_backends + [LabFilter]
    serializer_class = SubmissionTypeSerializer
    permission_classes = [SubmissionTypePermissions]
    permission_classes_by_action = {'validate_data': [AllowAny]}
    search_fields = ('name', 'description')
    filter_fields = {'active':['exact']}
    lab_filter = 'lab__lab_id'
#     def get_queryset(self):
#         return viewsets.ModelViewSet.get_queryset(self)
#         queryset = viewsets.ModelViewSet.get_queryset(self)
#         lab = get_site_lab(self.request)
#         return queryset.filter(lab=lab)
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
#     def perform_create(self, serializer):
#         return serializer.save(lab=get_site_lab(self.request))
    @action(detail=False, methods=['get'])
    def get_submission_schema(self, request):
        url = request.query_params.get('url')
        schema = get_submission_schema(url)
        return Response(schema)
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
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        submission = self.request.query_params.get('submission',None)
#         if self.request.user.is_authenticated:
#             return queryset
#         else:
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
    permission_classes = (NotePermissions,)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        submission = self.request.query_params.get('submission',None)
        if submission:
            submission = Submission.objects.filter(id=submission).first()
        if not submission:
            raise PermissionDenied('Must provide a submission id in the request.')
        queryset = queryset.filter(submission=submission)
        if not submission.lab.is_lab_member(self.request.user):
            queryset = queryset.filter(public=True)
        return queryset
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
    queryset = User.objects.all().order_by('last_name', 'first_name')
    serializer_class = UserSerializer
    ordering_fields = ['name','first_name','last_name']
    permission_classes = (IsAuthenticated,)
    filter_backends = viewsets.ModelViewSet.filter_backends + [UserFilter]
    filter_fields = {'is_staff':['exact'], 'labs__lab_id':['exact'], 'labs__id':['exact']}
    search_fields = ['first_name', 'last_name', 'email', 'username', 'emails__email']
    def get_serializer_class(self):
        return UserSerializer if self.detail else UserListSerializer
    @action(detail=False, methods=['post'])
    def update_settings(self,request):
        if not request.user.is_authenticated:
            return response.Response({'status':'error', 'message': 'You must log in to update settings.'},status=403)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        key = request.data.get('key', None)
        value = request.data.get('value', None)
        if not key or not value:
            return response.Response({'status':'error', 'message': 'Both "key" and "value" parameters are required'},status=403)
        profile.settings[key] = value
        profile.save()
        return response.Response({'status':'success', 'settings':profile.settings})
    @action(detail=False, methods=['get'])
    def get_token(self,request):
        if not request.user.is_authenticated:
            return response.Response({'status':'error', 'message': 'You must log in to get an API auth token.'}, status=403)
        token = Token.objects.filter(user=request.user).first()
        return response.Response({'status':'success', 'token':token.key if token else None})
    @action(detail=False, methods=['post'])
    def create_token(self,request):
        if not request.user.is_authenticated:
            return response.Response({'status':'error', 'message': 'You must log in to create an API auth token.'}, status=403)
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        return response.Response({'status':'success', 'token':token.key})
    @action(detail=False, methods=['delete'])
    def delete_token(self,request):
        if not request.user.is_authenticated:
            return response.Response({'status':'error', 'message': 'You must log in to delete an API auth token.'}, status=403)
        Token.objects.filter(user=request.user).delete()
        return response.Response({'status':'success', 'token':None})

#     @action(detail=False, methods=['post'])
#     def update_profile(self,request):
#         if not request.user.is_authenticated:
#             return response.Response({'status':'error', 'message': 'You must log in to update settings.'},status=403)
#         serializer = WritableUserSerializer(request.user, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
# class StatusViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = SubmissionStatus.objects.all().order_by('order')
#     serializer_class = StatusSerializer
#     ordering_fields = ['order']
#     permission_classes = (AllowAny,)

class UserEmailViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    @action(detail=False, methods=['post'])
    def claim(self, request):
        email = request.data.get('email', '')
        try:
            validate_email( email )
        except ValidationError:
            return response.Response({'status':'error', 'message': 'Please enter a valid email address.'}, status=403)
        user_email = UserEmail.objects.filter(email__iexact=email).first()
        if user_email:
            if user_email.user == request.user:
                return response.Response({'status':'error', 'message': 'You have already claimed email "{}".'.format(email)}, status=403)
            else:
                return response.Response({'status':'error', 'message': 'Email "{}" has already been claimed.'.format(email)}, status=403)
        email_token = str(uuid.uuid4())[-12:]
        request_id = str(uuid.uuid4())[-12:]
        request.session['email_request'] = {'email': email, 'token': email_token, 'request_id': request_id, 'requested': str(timezone.now())}
        claim_email(request, email, email_token)
        return response.Response({'status':'success', 'email': email, 'message': 'Please check email "{}" for a confirmation code'.format(email)})
    @action(detail=False, methods=['post'])
    def validate(self,request):
        token = request.data.get('token', '')
        email_request = request.session.get('email_request')
        if not email_request or token != email_request['token']:
            return response.Response({'status':'error', 'message': 'Provided token is invalid.'}, status=403)
        email = email_request['email']
        UserEmail.objects.create(user=request.user, email=email)
        del request.session['email_request']
        return response.Response({'status':'success', 'email': email, 'message': 'Email "{}" added to your account'.format(email)})
    @action(detail=False, methods=['post', 'get'])
    def set_primary(self,request):
        email = request.data.get('email', '')
        user_email = UserEmail.objects.get(user=request.user, email__iexact=email)
        user_email.user.email = user_email.email
        user_email.user.save()
        return response.Response({'status':'success', 'message': 'Email "{}" has been set as your primary email.'.format(email)})
class ValidatorViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        VALIDATORS_DICT.get(pk)
    def list(self, request):
        return response.Response([v.serialize() for v in VALIDATORS])

class DraftViewSet(viewsets.ModelViewSet):
    queryset = Draft.objects.all().order_by('-updated')
    serializer_class = DraftSerializer
    permission_classes = (DraftPermissions,)

class LabViewSet(PermissionMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Lab.objects.all()
#     serializer_class = LabListSerializer
    permission_classes = (IsLabMember,) # [LabObjectPermission.create(LabPermission.PERMISSION_ADMIN)]
    lookup_field = 'lab_id'
    permission_model = LabPermission
    manage_permissions_classes = [LabObjectPermission.create(LabPermission.PERMISSION_ADMIN)]
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return LabSerializer
        return LabSerializer if self.detail else LabListSerializer
    def get_queryset(self):
        queryset = viewsets.ModelViewSet.get_queryset(self)
        institution = get_site_institution(self.request)
        if self.request.user.is_staff:
            return queryset.filter(institution=institution)
        else:
            return queryset.filter(institution=institution, disabled=False)
#     @action(detail=False, methods=['get'])
#     def default(self, request):
#         lab = get_site_lab(request)
#         serializer = self.get_serializer(lab, many=False)
#         return Response(serializer.data)

class InstitutionViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = (IsSuperuserPermission,)
    permission_model = InstitutionPermission
    manage_permissions_classes = [InstitutionObjectPermission.create(InstitutionPermission.PERMISSION_ADMIN)]
    @action(detail=False, methods=['get'])
    def default(self, request):
        institution = get_site_institution(request)
        serializer = self.get_serializer(institution, many=False)
        return Response(serializer.data)
    

class ProjectIDViewSet(viewsets.ModelViewSet):
    queryset = ProjectID.objects.all()
    serializer_class = ProjectIDSerializer
    permission_classes = (ProjectIDPermissions,)
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

