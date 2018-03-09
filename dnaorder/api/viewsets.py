from rest_framework import viewsets
from dnaorder.api.serializers import SubmissionSerializer,\
    SubmissionFileSerializer
from dnaorder.models import Submission, SubmissionFile

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.select_related('type').all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'phone':['icontains'],'name':['icontains'],'email':['icontains'],'pi_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains']}
    ordering_fields = ['id', 'phone','name','email','pi_name','pi_email','institute','type__name','submitted']
#     def upload_file(self, request):
#         SubmissionFileSerializer
#         up_file = request.FILES['file']
#         destination = open('/Users/Username/' + up_file.name, 'wb+')
#         for chunk in up_file.chunks():
#             destination.write(chunk)
#             destination.close()
# 
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(up_file.name, status.HTTP_201_CREATED)
class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer
