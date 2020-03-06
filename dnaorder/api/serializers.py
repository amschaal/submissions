from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType, SubmissionFile,\
    SubmissionStatus, Note, Contact, Draft, Lab, PrefixID, Vocabulary, Term,\
    Import
import os
from django.contrib.auth.models import User
from dnaorder.validators import SamplesheetValidator, SubmissionValidator
from dnaorder.dafis import validate_dafis
from dnaorder import validators
from dnaorder.payment.ucd import UCDPaymentSerializer
from dnaorder.payment.ppms.serializers import PPMSPaymentSerializer
from rest_framework.exceptions import ValidationError

def translate_schema_complex(schema):
    if not  'order' in schema  or not  'properties' in schema :
        return schema
    new_schema = {'fields':[]}
    if  'layout' in schema :
        new_schema['layout'] = schema['layout']
    for v in schema['order']:
        s = schema['properties'][v]
        ns = {'id':v,'description':s.get('description'),'type':s.get('type'),'unique':s.get('unique',False),'required': v in schema.get('required',[]),'validators':[]}
        if  'enum' in s :
            ns['enum'] = s['enum']
        if ns['type'] == 'number':
            validator = {'id':validators.NumberValidator.id,'options':{'minimum':s.get('minimum'),'maximum':s.get('maximum')}}
            ns['validators'].append(validator)
        if ns['type'] == 'string' and  'pattern' in s :
            ns['validators'].append({'id':validators.RegexValidator.id,'options':{'regex':s['pattern']}})
        new_schema['fields'].append(ns)
    return new_schema

def translate_schema(schema):
    if not  'order' in schema  or not  'properties' in schema :
        return schema
    for v, s in schema['properties'].items():
        if not  'validators' in s :
            s['validators'] = []
#         ns = {'id':v,'description':s.get('description'),'type':s.get('type'),'unique':s.get('unique',False),'required': v in schema.get('required',[]),'validators':[]}
#         if ns['type'] == 'number':
#             validator = {'id':validators.NumberValidator.id,'options':{'minimum':s.get('minimum'),'maximum':s.get('maximum')}}
#             ns['validators'].append(validator)
#         if ns['type'] == 'string' and  'pattern' in s :
#             ns['validators'].append({'id':validators.RegexValidator.id,'options':{'regex':s['pattern']}})
#         new_schema['fields'].append(ns)
#     return new_schema

#Allows Creation/Updating of related model fields with OBJECT instead of just id
# Example: User = ModelRelatedField(model=User,serializer=UserSerializer,required=False,allow_null=True)
class ModelRelatedField(serializers.RelatedField):
    model = None
    pk = 'id'
    serializer = None
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', self.model)
        self.pk = kwargs.pop('pk', self.pk)
        self.serializer = kwargs.pop('serializer', self.serializer)
        assert self.model is not None, (
            'Must set model for ModelRelatedField'
        )
        assert self.serializer is not None, (
            'Must set serializer for ModelRelatedField'
        )
        self.queryset = kwargs.pop('queryset', self.model.objects.all())
        super(ModelRelatedField, self).__init__(**kwargs)
    def to_internal_value(self, data):
        if isinstance(data, int) or isinstance(data, str):
            kwargs = {self.pk:data}
            return self.model.objects.get(**kwargs)
        if data.get(self.pk,None):
            return self.model.objects.get(id=data['id'])
        return None
    def to_representation(self, value):
        return self.serializer(value).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class SubmissionTypeSerializer(serializers.ModelSerializer):
    submission_count = serializers.IntegerField(read_only=True)
#     submission_schema = serializers.SerializerMethodField()
#     sample_schema = serializers.SerializerMethodField()
#     def get_submission_schema(self,instance):
#         translate_schema(instance.submission_schema)
#         return instance.schema
#     def get_sample_schema(self,instance):
#         translate_schema(instance.sample_schema)
#         return instance.sample_schema
    def validate_examples(self, data):
        sample_schema = self.initial_data.get('sample_schema',{})
        validator = SamplesheetValidator(sample_schema, data)
        errors, warnings = validator.validate()
        if len(errors):
            raise serializers.ValidationError('Examples did not validate.')
#             
#             self.add_error('sample_data', 'Errors were found in the samplesheet')
#                 self.errors['_sample_data'] = errors
#         raise serializers.ValidationError('Examples did not validate.')
        return data
        # Apply custom validation either here, or in the view.
    class Meta:
        model = SubmissionType
        fields = ['id','lab','active','prefix','next_id','name','description','statuses','sort_order','submission_schema','sample_schema','submission_help','sample_help','updated','submission_count','confirmation_text', 'default_participants']
        read_only_fields = ('updated','lab')

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Contact
        exclude = ['submission']
        read_only_fields = ('id',)

class SubmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = ['id','name']

class WritableSubmissionSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        super(WritableSubmissionSerializer, self).__init__(*args, **kwargs)
    contacts = ContactSerializer(many=True)
    editable = serializers.SerializerMethodField()
#     warnings = serializers.SerializerMethodField()
#     payment_info = serializers.CharField(allow_null=True, allow_blank=True, default='')
    payment = UCDPaymentSerializer() #PPMSPaymentSerializer()# PPMSPaymentSerializer() 
#     def validate_payment_info(self, payment_info):
#         payment_type = self.initial_data.get('payment_type')
#         if payment_type == Submission.PAYMENT_CREDIT_CARD and payment_info:
#             raise serializers.ValidationError("Do not enter anything into payment info when choosing credit card!")
#         elif payment_type == Submission.PAYMENT_DAFIS:
#             if not validate_dafis(payment_info):
#                 raise serializers.ValidationError("The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'.")
#         elif payment_type in [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO] and not payment_info:
#             raise serializers.ValidationError("Please enter payment details.")
#         return payment_info
    def validate_sample_data(self, sample_data):
        schema = None
        type = self.initial_data.get('type')
        if self.instance:
            schema = self.instance.sample_schema
        elif type:
            type = SubmissionType.objects.get(id=type)
            schema = type.sample_schema
#         raise Exception(schema)
        
        if (not sample_data or len(sample_data) < 1) and schema and len(schema.get('order', [])) > 0:
            raise serializers.ValidationError("Please provide at least 1 sample.")
        
        if schema:
            validator = SamplesheetValidator(schema,sample_data)
            self._sample_errors, self._sample_warnings = validator.validate()
            if len(self._sample_errors):
                raise serializers.ValidationError(self._sample_errors)
            return validator.cleaned()
        return sample_data
    def validate_submission_data(self, data={}):
        type = self.initial_data.get('type')
        schema = None
        if self.instance:
            schema = self.instance.submission_schema
        elif type:
            type = SubmissionType.objects.get(id=type)
            schema = type.submission_schema
        if schema:
            validator = SubmissionValidator(schema,data)
            self._submission_errors, self._submission_warnings = validator.validate()
            if len(self._submission_errors):
                raise serializers.ValidationError(self._submission_errors)
            return validator.cleaned()
        return data
    def validate_import_data(self, data=None):
        if data:
            for f in ['lab', 'participants']:
                if f in data:
                    del data[f]
            return data
    def get_warnings(self):
        data = {}
        if hasattr(self, '_sample_warnings') and len(self._sample_warnings):
            data['sample_data']=self._sample_warnings
        if hasattr(self, '_submission_warnings') and len(self._submission_warnings):
            data['submission_data']=self._submission_warnings
#         if len(data) > 0:
#             raise serializers.ValidationError(data)
        return data
    def validate_warnings(self, data=None):
        data = self.get_warnings()
        return data if len(data) > 0 else None
#     def update_errors_and_warnings(self, instance):
#         print('SUBMISSION WARNINGS!!!', self._submission_warnings)
#         if not self.warnings and (len(self._sample_warnings) or len(self._submission_warnings)):
#             instance.warnings= {'submission_data':{},'sample_data':{}}
# #         if len(self._sample_errors):
# #             instance.data['errors']['sample_data']=self._sample_errors
#         if len(self._sample_warnings):
#             instance.warnings['sample_data']=self._sample_warnings
# #         if len(self._submission_errors):
# #             instance.data['errors']['submission_data']=self._submission_errors
#         if len(self._submission_warnings):
#             instance.warnings['submission_data']=self._submission_warnings
#         instance.save()
    def create(self, validated_data):
        contacts = validated_data.pop('contacts')
        validated_data['data'] = {
                                    'sample_data': {'errors':self._sample_errors, 'warnings': self._sample_warnings},
                                    'submission_data': {'errors':self._submission_errors, 'warnings': self._submission_warnings}
                                  }
        if validated_data.get('import_data', None):
            import_request = Import.objects.filter(id=validated_data['import_data'].get('id',None)).order_by('-created').first()
            validated_data['import_request'] = import_request
        submission = Submission.objects.create(**validated_data)
#         self.update_errors_and_warnings(submission)
        for contact in contacts:
            Contact.objects.create(submission=submission, **contact)
        return submission
    def update(self, instance, validated_data):
        contacts = validated_data.pop('contacts')
        info = serializers.model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
#         self.update_errors_and_warnings(instance)
        instance.save()
        
        Contact.objects.filter(submission=instance).exclude(id__in=[c.get('id') for c in contacts if c.get('id', False)]).delete()
        for c in contacts:
            if c.get('id', False):
                Contact.objects.filter(id=c.get('id'),submission=instance).update(**c)
            else:
                Contact.objects.create(submission=instance, **c)
        return instance
#     def update(self, instance, validated_data):
#         return super(WritableSubmissionSerializer, self).update(instance, validated_data)
#     def clean(self):
#         cleaned_data = super(SubmissionForm, self).clean()
#         sample_data = cleaned_data.get('sample_data')
#         type = cleaned_data.get('type')
#         if type and sample_data and len(sample_data) > 0:
#             validator = SamplesheetValidator(type.sample_schema,sample_data)
#             errors = validator.validate()
#             if len(errors):
#                 self.add_error('sample_data', 'Errors were found in the samplesheet')
#                 self.errors['_sample_data'] = errors
    def get_editable(self,instance):
        request = self._context.get('request')
        if request:
            return instance.editable(request.user)
#     def get_warnings(self, instance):
#         return instance.data.get('warnings') if instance and instance.data else {}
#     def validate(self, data):
#         print("VALIDATE!!!!!", data)
#         raise serializers.ValidationError({"warnings": {"foo":"bar"}})
#         return data
    def is_valid(self, raise_exception=False):
        valid = serializers.ModelSerializer.is_valid(self, raise_exception=False)
        print('is_valid 1', self.initial_data.keys())
        # Needs "if warnings and not ignore_warnings or not valid"
        
        if not valid or not self.initial_data.get('ignore_warnings',False):
            warnings = self.get_warnings()
            if warnings: # need to have a special parameter to ignore warnings if no errors exist
                if not hasattr(self, '_errors'):
                    self._errors = {}
                self._errors['warnings'] = warnings
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return valid
    class Meta:
        model = Submission
        exclude = ['submitted','sra_data','status','internal_id']
        read_only_fields= ['lab','data']

    """
        first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20)
    pi_first_name = models.CharField(max_length=50)
    pi_last_name = models.CharField(max_length=50)
    pi_email = models.EmailField(max_length=75)
    pi_phone = models.CharField(max_length=20)
    institute = models.CharField(max_length=75)
#     payment_type = models.CharField(max_length=50,choices=PAYMENT_CHOICES)
#     payment_info = models.CharField(max_length=250,null=True,blank=True)
    type = models.ForeignKey(SubmissionType,related_name="submissions", on_delete=models.PROTECT)
    submission_schema = JSONField(null=True,blank=True)
    sample_schema = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    sample_data = JSONField(null=True,blank=True)
    sra_data = JSONField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True) #Not really being used in interface?  Should be for admins.
    biocore = models.BooleanField(default=False)
    participants = models.ManyToManyField(User,blank=True)
    data = JSONField(default=dict)
    payment = JSONField(default=dict)
    comments = models.TextField(null=True, blank=True)
    """
class ImportSubmissionSerializer(WritableSubmissionSerializer):
    def __init__(self, data, *args, **kwargs):
        print('ImportSubmissionSerializer', data, args, kwargs)
        self.type = kwargs.pop('type', None)
        data['type'] = data['type']['id']
        if self.type:
            data['type'] = self.type
#         del data['type']
        super(ImportSubmissionSerializer, self).__init__(*args, data=data, **kwargs)
    def validate_type(self, type):
        print('!!!!!!validate_type!!!!!', type)
        return type
        
    def update(self, instance, validated_data):
        raise NotImplementedError
    class Meta:
        model = Submission
        exclude = ['submitted','sra_data','status','internal_id','participants']
        read_only_fields= ['lab','data']

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        exclude = []
        read_only_fields = ('name', 'site', 'payment_type_id')

class SubmissionSerializer(WritableSubmissionSerializer):
#     def __init__(self, *args, **kwargs):
#         super(SubmissionSerializer, self).__init__(*args, **kwargs)
    type = SubmissionTypeSerializer()
    lab = LabSerializer(read_only=True)
#     status = SubmissionStatusSerializer()
    permissions = serializers.SerializerMethodField(read_only=True)
    participant_names = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    received_by_name = serializers.SerializerMethodField(read_only=True)
    def get_participant_names(self,instance):
        return ['{0} {1}'.format(p.first_name, p.last_name) for p in instance.participants.all()]
    def get_received_by_name(self,instance):
        return str(instance.received_by) if instance.received_by else None
    def get_url(self, instance):
        return instance.get_absolute_url(full_url=True)
    def get_permissions(self,instance):
        #Only return permissions for detailed view, otherwise too expensive
        if  'view' in self._context  and self._context['view'].detail and  'request' in self._context :
            return instance.get_user_permissions(self.context['request'].user)
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

class ImportSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField()
    def get_submissions(self, obj):
        return [{'id': s.id, 'internal_id': s.internal_id} for s in obj.submissions.all()]
    class Meta:
        model = Import
        exclude = []
        read_only_fields = ('id','created')


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        exclude = []
        read_only_fields = ('id','created','updated')
        
class PrefixSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefixID
        exclude = []
        read_only_fields = ('lab',)
        
class NoteSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        data = kwargs.get('data')
        if data:
            submission = Submission.objects.get(id=kwargs['data'].get('submission'))
            request = kwargs['context'].get('request')
            data.update({'created_by':request.user.id})
            if request.user.is_authenticated:
                if data.get('send_email'):
                    data.update({'emails':submission.get_submitter_emails()}) # submission.participant_emails
            else:
                data.update({'emails': submission.get_participant_emails()})
        return super(NoteSerializer, self).__init__(*args,**kwargs)
    user = serializers.SerializerMethodField()
    can_modify = serializers.SerializerMethodField()
    def get_user(self,instance):
        return str(instance.created_by) if instance.created_by else 'Anonymous'
    def get_can_modify(self,instance):
        request = self._context.get('request')
        if request:
            return instance.can_modify(request.user)
    class Meta:
        model = Note
        exclude = []

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = ['id', 'order', 'name']
        
class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = []

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        exclude = []