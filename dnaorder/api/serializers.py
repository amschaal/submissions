from rest_framework import serializers
from dnaorder.models import Submission
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        exclude = []