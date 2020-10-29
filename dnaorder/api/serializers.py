from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType, SubmissionFile,\
    Note, Contact, Draft, Lab, Vocabulary, Term,\
    Import, UserProfile, Sample, Institution, ProjectID
import os
from django.contrib.auth.models import User
from dnaorder.validators import SamplesheetValidator, SubmissionValidator
from dnaorder.dafis import validate_dafis
from dnaorder import validators
from dnaorder.payment.ucd import UCDPaymentSerializer
from dnaorder.payment.ppms.serializers import PPMSPaymentSerializer
from rest_framework.exceptions import ValidationError
import profile
from openpyxl.cell import read_only
from random import sample
from django.db import transaction
from schema.utils import Schema
from _collections import OrderedDict
from dnaorder.utils import assign_submission

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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

class LabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['name', 'id', 'lab_id']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    labs = LabListSerializer(read_only=True, many=True)
    emails = serializers.SerializerMethodField()
    def get_emails(self, instance):
        return [e.email for e in instance.emails.all()]
    class Meta:
        model = User
        exclude = ['password']

class UserListSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class WritableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

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
#     def validate_examples(self, data):
#         sample_schema = self.initial_data.get('sample_schema',{})
#         validator = SamplesheetValidator(sample_schema, data)
#         errors, warnings = validator.validate()
#         if len(errors):
#             raise serializers.ValidationError('Examples did not validate.')
# #             
# #             self.add_error('sample_data', 'Errors were found in the samplesheet')
# #                 self.errors['_sample_data'] = errors
# #         raise serializers.ValidationError('Examples did not validate.')
#         return data
        # Apply custom validation either here, or in the view.
    class Meta:
        model = SubmissionType
        fields = ['id', 'prefix','lab','active', 'default_id','name','description','statuses','sort_order','submission_schema','submission_help','updated','submission_count','confirmation_text', 'default_participants']
        read_only_fields = ('updated',)

class SimpleSubmissionTypeSerializer(SubmissionTypeSerializer):
    pass
    class Meta:
        model = SubmissionType
        fields = ['id', 'prefix', 'name', 'statuses']
        read_only_fields = ('updated',)

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Contact
        exclude = ['submission']
        read_only_fields = ('id',)

# class SubmissionStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubmissionStatus
#         fields = ['id','name']

# class SamplesField(serializers.Field):
#     def to_representation(self, value):
#         if hasattr(self, 'parent') and hasattr(self.parent,'instance'):
#             value = [s.data for s in Sample.objects.filter(submission=self.parent.instance).order_by('row')]
#         return value
#     def to_internal_value(self, data):
#         return data

class WritableSubmissionSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    editable = serializers.SerializerMethodField()
    payment = UCDPaymentSerializer() #PPMSPaymentSerializer()# PPMSPaymentSerializer()
    participants = UserListSerializer(many=True, read_only=True)
    #temporarily disable the following serializer
#     sample_data = SamplesField() #serializers.SerializerMethodField(read_only=False)
    table_count = serializers.SerializerMethodField()
    def get_table_count(self,instance):
        schema = Schema(instance.submission_schema)
        tables = OrderedDict([(v,instance.submission_data.get(v)) for v in schema.table_variables])
        return {schema.variable_title(v):len(d) if isinstance(d, list) else 0 for v,d in tables.items()}
#     def validate_sample_data(self, sample_data):
#         schema = None
#         type = self.initial_data.get('type')
#         if self.instance:
#             schema = self.instance.sample_schema
#         elif type:
#             type = SubmissionType.objects.get(id=type)
#             schema = type.sample_schema
# #         raise Exception(schema)
#         
#         if (not sample_data or len(sample_data) < 1) and schema and len(schema.get('order', [])) > 0:
#             raise serializers.ValidationError("Please provide at least 1 sample.")
#         
#         if schema:
#             validator = SamplesheetValidator(schema,sample_data)
#             self._sample_errors, self._sample_warnings = validator.validate()
#             if len(self._sample_errors):
#                 raise serializers.ValidationError(self._sample_errors)
#             return validator.cleaned()
#         return sample_data
    def validate_submission_data(self, data={}):
        type = self.initial_data.get('type')
        schema = None
        if self.instance:
            schema = self.instance.submission_schema
        elif type:
            self._type = SubmissionType.objects.get(id=type)
            schema = self._type.submission_schema
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
#         if hasattr(self, '_sample_warnings') and len(self._sample_warnings):
#             data['sample_data']=self._sample_warnings
        if hasattr(self, '_submission_warnings') and len(self._submission_warnings):
            data['submission_data']=self._submission_warnings
        return data
    def validate_warnings(self, data=None):
        #don't raise errors in here, only in is_valid
        data = self.get_warnings()
        return data if len(data) > 0 else None
    def create(self, validated_data):
        with transaction.atomic():
            contacts = validated_data.pop('contacts')
            validated_data['data'] = {
#                                         'sample_data': {'errors':self._sample_errors, 'warnings': self._sample_warnings},
                                        'submission_data': {'errors':self._submission_errors, 'warnings': self._submission_warnings}
                                      }
            if validated_data.get('import_data', None):
                import_request = Import.objects.filter(id=validated_data['import_data'].get('id',None)).order_by('-created').first()
                validated_data['import_request'] = import_request
#             if hasattr(self, '_type'):
            validated_data['lab'] = self._type.lab
            submission = Submission.objects.create(**validated_data)
#             submission.update_samples(validated_data.pop('sample_data'))
    #         self.update_errors_and_warnings(submission)
            for contact in contacts:
                Contact.objects.create(submission=submission, **contact)
            assign_submission(submission)
            return submission
    def update(self, instance, validated_data):
        with transaction.atomic():
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
            
#             instance.update_samples(validated_data.pop('sample_data'))
                
            Contact.objects.filter(submission=instance).exclude(id__in=[c.get('id') for c in contacts if c.get('id', False)]).delete()
            for c in contacts:
                if c.get('id', False):
                    Contact.objects.filter(id=c.get('id'),submission=instance).update(**c)
                else:
                    Contact.objects.create(submission=instance, **c)
            assign_submission(instance)
            return instance
    def get_editable(self,instance):
        request = self._context.get('request')
        if request:
            return instance.editable(request.user)
    def is_valid(self, raise_exception=False):
        valid = serializers.ModelSerializer.is_valid(self, raise_exception=False)
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
        exclude = ['submitted','status','internal_id','users','sample_data', 'sample_schema']
        read_only_fields= ['lab','data', 'participants']

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
        exclude = ['submitted','status','internal_id','participants']
        read_only_fields= ['lab','data']

class LabSerializer(serializers.ModelSerializer):
    submission_types = serializers.SerializerMethodField(read_only=True)
    users = ModelRelatedField(model=User,serializer=UserListSerializer,many=True,required=False,allow_null=True)
    def __init__(self, *args, **kwargs):
        super(LabSerializer, self).__init__(*args, **kwargs)
        self.is_lab_member = False
        if 'request' in self._context and hasattr(self, 'instance'):
            self.is_lab_member = self.instance.is_lab_member(self._context['request'].user)
    def get_fields(self):
#         print('get fields: instance', self.instance)
        fields = serializers.ModelSerializer.get_fields(self)
        if not self.is_lab_member:
            for k in ['payment_type_id', 'statuses', 'submission_email_text', 'submission_variables', 'table_variables', 'users']:
                if k in fields:
                    del fields[k]
        return fields
    def get_submission_types(self, obj):
        # Only return inactive types for lab members
        if 'request' in self._context and obj.is_lab_member(self._context['request'].user):
            types = obj.submission_types.all()
        else:
            types = obj.submission_types.filter(active=True)
        return SubmissionTypeSerializer(types, many=True, read_only=True).data
    class Meta:
        model = Lab
        exclude = ['institution']
        read_only_fields = ('name', 'site', 'payment_type_id', 'submission_types', 'disabled')

        
class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        exclude = []
        read_only_fields = ('name', 'site')

class SubmissionSerializer(WritableSubmissionSerializer):
#     def __init__(self, *args, **kwargs):
#         super(SubmissionSerializer, self).__init__(*args, **kwargs)
    type = SimpleSubmissionTypeSerializer() #SubmissionTypeSerializer()
    lab = LabSerializer(read_only=True)
#     status = SubmissionStatusSerializer()
    permissions = serializers.SerializerMethodField(read_only=True)
    participant_names = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    received_by_name = serializers.SerializerMethodField(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    def get_participant_names(self,instance):
        return ['{0} {1}'.format(p.first_name, p.last_name) for p in instance.participants.all().order_by('last_name', 'first_name')]
    def get_received_by_name(self,instance):
        return str(instance.received_by) if instance.received_by else None
    def get_url(self, instance):
        return instance.get_absolute_url(full_url=True)
    def get_permissions(self,instance):
        #Only return permissions for detailed view, otherwise too expensive
        if  'view' in self._context  and self._context['view'].detail and  'request' in self._context :
            return instance.permissions(self.context['request'].user)
    class Meta:
        model = Submission
        exclude = ['sample_data', 'sample_schema']

# A more efficent serializer for lists.  Limit attributes with large data or querying.
class ListSubmissionSerializer(SubmissionSerializer):
    sample_data = None
    lab = LabListSerializer(read_only=True)
    class Meta:
        model = Submission
        exclude = ['sample_data', 'submission_schema', 'sample_schema', 'import_data']
        
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
        
class ProjectIDSerializer(serializers.ModelSerializer):
    generate_id = serializers.CharField(read_only=True)
    class Meta:
        model = ProjectID
        exclude = []
#         read_only_fields = ('lab',)
        
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

# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubmissionStatus
#         fields = ['id', 'order', 'name']
        
class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = []

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        exclude = []