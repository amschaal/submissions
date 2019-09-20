from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType, SubmissionFile,\
    SubmissionStatus, Note, Contact, Draft, Lab, PrefixID, Vocabulary, Term
import os
from django.contrib.auth.models import User
from dnaorder.validators import SamplesheetValidator, SubmissionValidator
from dnaorder.dafis import validate_dafis
from dnaorder import validators
from dnaorder.payment.ucd import UCDPaymentSerializer
from dnaorder.payment.ppms.serializers import PPMSPaymentSerializer

def translate_schema_complex(schema):
    if not schema.has_key('order') or not schema.has_key('properties'):
        return schema
    new_schema = {'fields':[]}
    if schema.has_key('layout'):
        new_schema['layout'] = schema['layout']
    for v in schema['order']:
        s = schema['properties'][v]
        ns = {'id':v,'description':s.get('description'),'type':s.get('type'),'unique':s.get('unique',False),'required': v in schema.get('required',[]),'validators':[]}
        if s.has_key('enum'):
            ns['enum'] = s['enum']
        if ns['type'] == 'number':
            validator = {'id':validators.NumberValidator.id,'options':{'minimum':s.get('minimum'),'maximum':s.get('maximum')}}
            ns['validators'].append(validator)
        if ns['type'] == 'string' and s.has_key('pattern'):
            ns['validators'].append({'id':validators.RegexValidator.id,'options':{'regex':s['pattern']}})
        new_schema['fields'].append(ns)
    return new_schema

def translate_schema(schema):
    if not schema.has_key('order') or not schema.has_key('properties'):
        return schema
    for v, s in schema['properties'].items():
        if not s.has_key('validators'):
            s['validators'] = []
#         ns = {'id':v,'description':s.get('description'),'type':s.get('type'),'unique':s.get('unique',False),'required': v in schema.get('required',[]),'validators':[]}
#         if ns['type'] == 'number':
#             validator = {'id':validators.NumberValidator.id,'options':{'minimum':s.get('minimum'),'maximum':s.get('maximum')}}
#             ns['validators'].append(validator)
#         if ns['type'] == 'string' and s.has_key('pattern'):
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
        if isinstance(data, int) or isinstance(data, basestring):
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
#         print 'WriteableSubmissionSerializer'
#         print args
#         print kwargs
        super(WritableSubmissionSerializer, self).__init__(*args, **kwargs)
    contacts = ContactSerializer(many=True)
    editable = serializers.SerializerMethodField()
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
        if not sample_data or len(sample_data) < 1:
            raise serializers.ValidationError("Please provide at least 1 sample.")
        type = self.initial_data.get('type')
        schema = None
        if self.instance:
            schema = self.instance.sample_schema
        elif type:
            type = SubmissionType.objects.get(id=type)
            schema = type.sample_schema
        if schema:
            validator = SamplesheetValidator(schema,sample_data)
            errors = validator.validate()
            if len(errors):
                raise serializers.ValidationError("Samplesheet contains errors.")
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
            errors = validator.validate()
            if len(errors.keys()):
                raise serializers.ValidationError(errors)
            return validator.cleaned()
        return data
    def create(self, validated_data):
        print 'creating'
        print validated_data
        contacts = validated_data.pop('contacts')
        submission = Submission.objects.create(**validated_data)
        for contact in contacts:
            Contact.objects.create(submission=submission, **contact)
        return submission
    def update(self, instance, validated_data):
        contacts = validated_data.pop('contacts')
        print 'updating'
        print instance
        print contacts
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
        instance.save()
        Contact.objects.filter(submission=instance).exclude(id__in=[c.get('id') for c in contacts if c.get('id', False)]).delete()
        for c in contacts:
            if c.get('id', False):
                Contact.objects.filter(id=c.get('id'),submission=instance).update(**c)
            else:
                Contact.objects.create(submission=instance, **c)
        return instance
#     def update(self, instance, validated_data):
#         print 'updating'
#         print validated_data
#         return super(WritableSubmissionSerializer, self).update(instance, validated_data)
#     def clean(self):
#         cleaned_data = super(SubmissionForm, self).clean()
#         sample_data = cleaned_data.get('sample_data')
#         type = cleaned_data.get('type')
# #         print 'sample_data'
# #         print sample_data
#         if type and sample_data and len(sample_data) > 0:
#             validator = SamplesheetValidator(type.sample_schema,sample_data)
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
        exclude = ['submitted','sra_data','status','internal_id','data']
        read_only_fields= ['lab']
        
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        exclude = []
        read_only_fields = ('name', 'site', 'payment_type_id')

class SubmissionSerializer(WritableSubmissionSerializer):
#     def __init__(self, *args, **kwargs):
#         print 'submissionserializers'
#         print args
#         print kwargs
#         super(SubmissionSerializer, self).__init__(*args, **kwargs)
    type = SubmissionTypeSerializer()
    lab = LabSerializer(read_only=True)
#     status = SubmissionStatusSerializer()
    permissions = serializers.SerializerMethodField(read_only=True)
    participant_names = serializers.SerializerMethodField(read_only=True)
    def get_participant_names(self,instance):
        return ['{0} {1}'.format(p.first_name, p.last_name) for p in instance.participants.all()]
    def get_permissions(self,instance):
        #Only return permissions for detailed view, otherwise too expensive
        if self._context.has_key('view') and self._context['view'].detail and self._context.has_key('request'):
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
        print data
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