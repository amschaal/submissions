from rest_framework import viewsets
from dnaorder.api.serializers import SubmissionSerializer
from dnaorder.models import Submission

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_fields = {'id':['icontains','exact'],'phone':['icontains']}