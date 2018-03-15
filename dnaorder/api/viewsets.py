from rest_framework import viewsets, response
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer
from dnaorder.models import Submission, SubmissionFile, SubmissionStatus
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from dnaorder.api.permissions import SubmissionFilePermissions

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.select_related('type','status').all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'phone':['icontains'],'name':['icontains'],'email':['icontains'],'pi_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status__name':['icontains']}
    ordering_fields = ['id', 'phone','name','email','pi_name','pi_email','institute','type__name','submitted','status__order']
    @detail_route(methods=['post'])
    def update_status(self,request,pk):
        submission = self.get_object()
        submission.status = SubmissionStatus.objects.get(id=request.data.get('status'))
        submission.save()
        return response.Response({'status':'success','message':'Status updated.'})

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
