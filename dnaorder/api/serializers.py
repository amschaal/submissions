from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType, SubmissionFile,\
    SubmissionStatus, Note
import os
from django.contrib.auth.models import User
from dnaorder.validators import SamplesheetValidator
from dnaorder.dafis import validate_dafis

class SubmissionTypeSerializer(serializers.ModelSerializer):
    submission_count = serializers.IntegerField(read_only=True)
    def validate_examples(self, data):
        schema = self.initial_data.get('schema',{})
        validator = SamplesheetValidator(schema, data)
        errors = validator.validate()
        print errors
        if len(errors):
            raise serializers.ValidationError('Examples did not validate.')
#             
#             self.add_error('sample_data', 'Errors were found in the samplesheet')
#                 self.errors['_sample_data'] = errors
#         print data
#         print self.initial_data
#         raise serializers.ValidationError('Examples did not validate.')
        return data
        # Apply custom validation either here, or in the view.
    class Meta:
        model = SubmissionType
        fields = ['id','name','description','schema','examples','help','updated','submission_count']
        read_only_fields = ('updated',)

class SubmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = ['id','name']

class WritableSubmissionSerializer(serializers.ModelSerializer):
    editable = serializers.SerializerMethodField()
    payment_info = serializers.CharField(allow_null=True, allow_blank=True, default='')
    def validate_payment_info(self, payment_info):
        payment_type = self.initial_data.get('payment_type')
        if payment_type == Submission.PAYMENT_CREDIT_CARD and payment_info:
            raise serializers.ValidationError("Do not enter anything into payment info when choosing credit card!")
        elif payment_type == Submission.PAYMENT_DAFIS:
            if not validate_dafis(payment_info):
                raise serializers.ValidationError("The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'.")
        elif payment_type in [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO] and not payment_info:
            raise serializers.ValidationError("Please enter payment details.")
        return payment_info
    def validate_sample_data(self, sample_data):
        if not sample_data or len(sample_data) < 1:
            raise serializers.ValidationError("Please provide at least 1 sample.")
        type = self.initial_data.get('type')
        if type and sample_data and len(sample_data) > 0:
            type = SubmissionType.objects.get(id=type)
            validator = SamplesheetValidator(type.schema,sample_data)
            errors = validator.validate()
            if len(errors):
                raise serializers.ValidationError("Samplesheet contains errors.")
        return sample_data
#     def clean(self):
#         cleaned_data = super(SubmissionForm, self).clean()
#         sample_data = cleaned_data.get('sample_data')
#         type = cleaned_data.get('type')
# #         print 'sample_data'
# #         print sample_data
#         if type and sample_data and len(sample_data) > 0:
#             validator = SamplesheetValidator(type.schema,sample_data)
#             errors = validator.validate()
#             print errors
#             if len(errors):
#                 self.add_error('sample_data', 'Errors were found in the samplesheet')
#                 self.errors['_sample_data'] = errors
    def get_editable(self,instance):
        request = self._context.get('request')
        if request:
            return instance.editable(request.user)
    class Meta:
        model = Submission
        exclude = ['submitted','sra_data','status','internal_id','participants','data']

class SubmissionSerializer(WritableSubmissionSerializer):
    type = SubmissionTypeSerializer()
    status = SubmissionStatusSerializer()
    class Meta:
        model = Submission
        exclude = []

class SubmissionFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    def get_filename(self,instance):
        return os.path.basename(instance.file.name)
    def get_size(self,instance):
        return instance.formatted_size()
    def get_date(self,instance):
        return instance.formatted_date()
    class Meta:
        model = SubmissionFile
        exclude = []

class NoteSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        data = kwargs.get('data')
        if data:
            submission = Submission.objects.get(id=kwargs['data'].get('submission'))
            request = kwargs['context'].get('request')
            data.update({'created_by':request.user.id})
            if request.user.is_authenticated:
                if data.get('send_email'):
                    data.update({'emails':[submission.email]})
            else:
                data.update({'emails': submission.participant_emails})
        return super(NoteSerializer, self).__init__(*args,**kwargs)
    user = serializers.SerializerMethodField()
    can_modify = serializers.SerializerMethodField()
    def get_user(self,instance):
        return str(instance.created_by)
    def get_can_modify(self,instance):
        request = self._context.get('request')
        if request:
            return instance.can_modify(request.user)
    class Meta:
        model = Note
        exclude = []

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = ['id', 'order', 'name']