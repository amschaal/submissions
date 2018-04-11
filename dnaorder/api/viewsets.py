from rest_framework import viewsets, response
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer, NoteSerializer
from dnaorder.models import Submission, SubmissionFile, SubmissionStatus, Note
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from dnaorder.api.permissions import SubmissionFilePermissions
from django.core.mail import send_mail
from dnaorder import emails

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.select_related('type','status').all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'internal_id':['icontains','exact'],'phone':['icontains'],'name':['icontains'],'email':['icontains'],'pi_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status__name':['icontains'],'biocore':['exact']}
    ordering_fields = ['id','internal_id', 'phone','name','email','pi_name','pi_email','institute','type__name','submitted','status__order','biocore']
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

class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [SubmissionFilePermissions]
        return [permission() for permission in permission_classes]
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
        