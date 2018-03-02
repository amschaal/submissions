from rest_framework import viewsets
from dnaorder.api.serializers import SubmissionSerializer
from dnaorder.models import Submission

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.select_related('type').all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'phone':['icontains'],'name':['icontains'],'email':['icontains'],'pi_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains']}