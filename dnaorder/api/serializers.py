from rest_framework import serializers
from dnaorder.models import Submission, SubmissionType, SubmissionFile,\
    Note, Contact, Draft, Lab, Vocabulary, Term,\
    Import, UserProfile, Sample, Institution, ProjectID, LabPermission,\
    InstitutionPermission
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
from django.conf import settings
from plugins import PluginManager
from dnaorder.utils import get_site_institution

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
    # Need to only have plugins in detailed lab serializer for efficiency.  Frontend is currently getting it from the list of labs though. 
    plugins = serializers.SerializerMethodField(read_only=True)
    def get_plugins(self, instance):
        return instance.get_plugin_settings(private=False)
    class Meta:
        model = Lab
        fields = ['name', 'id', 'lab_id', 'plugins', 'disabled']
        read_only_fields = ['name', 'id', 'lab_id', 'plugins', 'disabled']

class InstitutionLabSerializer(LabListSerializer):
    class Meta:
        model = Lab
        fields = ['name', 'id', 'lab_id', 'disabled', 'plugins']
        read_only_fields = ['plugins']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    labs = serializers.SerializerMethodField() # LabListSerializer(read_only=True, many=True)
    emails = serializers.SerializerMethodField()
    def get_emails(self, instance):
        return [e.email for e in instance.emails.all()]
    def get_labs(self, instance):
        return LabListSerializer(Lab.objects.filter(permissions__user=instance).distinct(), many=True).data
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'emails', 'profile', 'labs', 'is_staff', 'is_superuser']
#         exclude = ['password', 'is_staff', 'groups', 'is_superuser']

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

class WritableSubmissionSerializer(serializers.ModelSerializer):
    def __init__(self,instance=None,**kwargs):
        # @todo: Hacky, need to clean up for cases where writing submission vs instance, vs queryset
        data = kwargs.get('data')
        payment_type_id = None
        if instance and hasattr(instance, 'type'):
            self._type = instance.type
            self._lab = instance.lab
            payment_type_id = instance.payment.get('plugin_id') # get payment_type_id from submission
        elif data:
            if data.get('type'):
                self._type = SubmissionType.objects.select_related('lab').get(id=data.get('type'))
                self._lab = self._type.lab
                payment_type_id = self._lab.payment_type_id # get payment_type_id from lab
        if hasattr(self, '_lab'):
            payment_type_plugin = PluginManager().get_payment_type(payment_type_id)
            if payment_type_plugin and payment_type_plugin.serializer:
                self.fields['payment'] = payment_type_plugin.serializer(plugin_id=payment_type_id, lab=self._lab)
        return super(WritableSubmissionSerializer, self).__init__(instance,**kwargs)
    contacts = ContactSerializer(many=True)
    editable = serializers.SerializerMethodField()
    payment = UCDPaymentSerializer() #PPMSPaymentSerializer()# UCDPaymentSerializer()
    participants = UserListSerializer(many=True, read_only=True)
    #temporarily disable the following serializer
#     sample_data = SamplesField() #serializers.SerializerMethodField(read_only=False)
    table_count = serializers.SerializerMethodField()
    def get_table_count(self,instance):
        schema = Schema(instance.submission_schema)
        tables = OrderedDict([(v,instance.submission_data.get(v)) for v in schema.table_variables])
        return {schema.variable_title(v):len(d) if isinstance(d, list) else 0 for v,d in tables.items()}
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
            validated_data['lab'] = self._type.lab
            submission = Submission.objects.create(**validated_data)
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
            instance.save()
                
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
    users = serializers.SerializerMethodField(read_only=True)
    user_permissions = serializers.SerializerMethodField(read_only=True)
    plugins = serializers.SerializerMethodField(read_only=True)
    def __init__(self, *args, **kwargs):
        super(LabSerializer, self).__init__(*args, **kwargs)
        self.is_lab_member = False
        if 'request' in self._context and hasattr(self, 'instance') and self.instance:
            self.is_lab_member = self.instance.is_lab_member(self._context['request'].user)
    def get_fields(self):
        fields = serializers.ModelSerializer.get_fields(self)
        if not self.is_lab_member:
            for k in ['payment_type_id', 'statuses', 'submission_email_text', 'submission_variables', 'table_variables', 'users']:
                if k in fields:
                    del fields[k]
        return fields
    def get_users(self, obj):
        # users = User.objects.filter(lab_permissions__permission_object=obj).distinct() #LabPermission.objects.filter()
        return UserListSerializer(obj.members, many=True).data
    def get_user_permissions(self, obj):
        if self._context['request'].user.is_superuser:
            return [c[0] for c in LabPermission.PERMISSION_CHOICES]
        elif self._context['request'].user and not self._context['request'].user.is_authenticated:
            return []
        else:
            return obj.permissions.filter(user=self._context['request'].user).values_list('permission', flat=True)
    def get_submission_types(self, obj):
        # Only return inactive types for lab members
        if 'request' in self._context and obj.is_lab_member(self._context['request'].user):
            types = obj.submission_types.all()
        else:
            types = obj.submission_types.filter(active=True)
        return SubmissionTypeSerializer(types, many=True, read_only=True).data
    def get_plugins(self, instance):
        return instance.get_plugin_settings(private=False)
        # admin = 'request' in self._context and hasattr(self, 'instance') and self.instance and self.instance.has_permission(self._context['request'].user, LabPermission.PERMISSION_ADMIN)
        # if admin: #don't filter for admins
        #     return instance.plugins 
        # else: #filter out private config
        #     plugins = {}
        #     for p, config in instance.plugins.items():
        #         plugins[p] = {}
        #         plugins[p]['public'] = config.get('public', {})
        #         plugins[p]['enabled'] = config.get('enabled', False)
        #     return plugins
    def create(self, validated_data):
        validated_data['institution'] =  get_site_institution(self.context['request'])
        return super().create(validated_data)
    class Meta:
        model = Lab
        exclude = ['institution']
        read_only_fields = ('site', 'payment_type_id', 'submission_types', 'disabled','plugins')

        
class InstitutionSerializer(serializers.ModelSerializer):
    # plugins = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Institution
        exclude = ['plugins']
        read_only_fields = ('site',)
    # def get_plugins(self, instance):
    #     # admin = 'request' in self._context and hasattr(self, 'instance') and self.instance and self.instance.has_permission(self._context['request'].user, InstitutionPermission.PERMISSION_ADMIN)
    #     admin = 'request' in self._context and self._context['request'].user.is_superuser
    #     if admin: #don't filter for admins
    #         return instance.plugins 
    #     else: #filter out private config
    #         plugins = {}
    #         for p, config in instance.plugins.items():
    #             plugins[p] = {}
    #             plugins[p]['public'] = config.get('public', {})
    #             plugins[p]['enabled'] = config.get('enabled', False)

class SubmissionSerializer(WritableSubmissionSerializer):
    type = SimpleSubmissionTypeSerializer() #SubmissionTypeSerializer()
    lab = LabListSerializer(read_only=True)
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
        exclude = ['sample_data', 'sample_schema','plugin_data']

# A more efficent serializer for lists.  Limit attributes with large data or querying.
class ListSubmissionSerializer(SubmissionSerializer):
    sample_data = None
    lab = LabListSerializer(read_only=True)
    class Meta:
        model = Submission
        exclude = ['sample_data', 'sample_schema', 'import_data']#, 'submission_schema'
        
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
            if request.user.is_authenticated and request.user.is_staff:
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

class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = []

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        exclude = []

class LabPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabPermission
        exclude = []

class InstitutionPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionPermission
        exclude = []