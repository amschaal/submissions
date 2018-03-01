from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType

class SubmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionType
        fields = ['id','name']

class SubmissionSerializer(serializers.ModelSerializer):
    type = SubmissionTypeSerializer(read_only=True)
    class Meta:
        model = Submission
        exclude = []