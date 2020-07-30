from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.fields.jsonb import JSONField
import re
import os
import datetime
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from dnaorder import emails
from django.contrib.postgres.fields.array import ArrayField
from django.contrib.sites.models import Site
from dnaorder.payment import PaymentTypeManager
from django.conf import settings
from django.db.models.query_utils import Q

def default_schema():
    return {'properties': {}, 'order': [], 'required': [], 'layout': {}}

# class PaymentType(models.Model):
#     id = models.CharField(max_length=30, primary_key=True) # ie: 'stratocore'|'Dafis'|...

class PrefixID(models.Model):
    lab = models.ForeignKey('Lab', null=True, related_name='prefixes', on_delete=models.CASCADE)
    prefix = models.CharField(max_length=15)
    current_id = models.PositiveIntegerField(default=0)
    def generate_id(self, minimum_digits=4):
        return '{prefix}{id}'.format(prefix=self.prefix,id=str(self.current_id).zfill(minimum_digits))
    def __str__(self):
        return self.generate_id()

class Institution(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=50)
    site = models.OneToOneField(Site, on_delete=models.PROTECT)

class InstitutionPermission(models.Model):
    PERMISSION_ADMIN = 'admin'
    PERMISSION_MANAGE = 'manage'
    PERMISSION_CHOICES = ((PERMISSION_ADMIN, 'Admin'), (PERMISSION_MANAGE, 'Manage'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

class Lab(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True)
    lab_id = models.SlugField(null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    site = models.OneToOneField(Site, on_delete=models.PROTECT)
    payment_type_id = models.CharField(max_length=30, choices=PaymentTypeManager().get_choices()) # validate against list of configured payment types
    home_page = models.TextField(default='')
    submission_page = models.TextField(default='', blank=True)
    statuses = JSONField(default=list)
    submission_variables = JSONField(default=dict)
    table_variables = JSONField(default=dict)
    users = models.ManyToManyField(User, related_name='labs')
#     def user_permissions(self, user):
#         permissions = []
#         if self.users.filter(id=user.id).exists():
#             permissions.append(LabPermission.PERMISSION_MANAGE_SUBMISSIONS, )
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (('institution', 'lab_id'))

class LabPermission(models.Model):
    PERMISSION_ADMIN = 'admin'
    PERMISSION_MANAGE_TYPES = 'manage_types'
    PERMISSION_MANAGE_SUBMISSIONS = 'manage_submissions'
    PERMISSION_CHOICES = ((PERMISSION_ADMIN, 'Admin'), (PERMISSION_MANAGE_TYPES, 'Manage submission types'), (PERMISSION_MANAGE_SUBMISSIONS, 'Manage submissions'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

class SubmissionType(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT, related_name='submission_types')
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,null=True,blank=True, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    sort_order = models.PositiveIntegerField(default=1)
    prefix = models.CharField(max_length=15)
    next_id = models.PositiveIntegerField(default=1)
    sample_identifier = models.CharField(max_length=25,default='sample_name')
    exclude_fields = models.TextField(blank=True)
    submission_help = models.TextField(null=True,blank=True)
    statuses = JSONField(default=list)
    submission_schema = JSONField(null=True,default=default_schema)
    sample_schema = JSONField(null=True,default=default_schema)
    sample_help = models.TextField(null=True, blank=True)
    confirmation_text = models.TextField(null=True, blank=True)
    default_participants = models.ManyToManyField(User, blank=True, related_name='+')
    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = (('lab','prefix'),)
    def get_next_id(self):
        return "{0}{1}".format(self.prefix, str(self.next_id).zfill(4))
    def get_previous_id(self):
        return "{0}{1}".format(self.prefix, str(self.next_id-1).zfill(4))
    def __str__(self):
        return "{name}".format(name=self.name)
#     @property
#     def samplesheet(self):
#         if not self.form or not self.id:
#             return None
#         from dnaorder.spreadsheets import CoreSampleSheet
#         return CoreSampleSheet(self.form.file,self)
    @property
    def excluded_fields(self):
        return [field.strip() for field in self.exclude_fields.split(',')] if self.exclude_fields else []

def submission_file_path(instance, filename):
    return 'submissions/{date:%Y}/{date:%m}/{submission_id}/{filename}'.format(date=instance.submission.submitted,submission_id=instance.submission.id,filename=filename)

def generate_id():
    while True:
        id = str(uuid.uuid4())[-12:]
        if not Submission.objects.filter(id=id).exists():
            return id

def generate_file_id():
    while True:
        id = str(uuid.uuid4())[-12:]
        if not SubmissionFile.objects.filter(id=id).exists():
            return id

# #Deprected/Obsolete: remove
# class SubmissionStatus(models.Model):
#     order = models.PositiveSmallIntegerField()
#     name = models.CharField(max_length=40)
#     auto_lock = models.BooleanField(default=False)
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural = "Submission Statuses"
#         ordering = ['order']

class Submission(models.Model):
#     STATUS_SUBMITTED = 'submitted'
#     STATUS_ACCEPTED = 'accepted'
#     STATUS_RECEIVED = 'received'
#     STATUS_PASSED_QC = 'passed_qc'
#     STATUS_LIBRARIES_PREPPED = 'libraries_prepped'
#     STATUS_DATA_AVAILABLE = 'data_available'
#     STATUS_CHOICES = (
#         (STATUS_SUBMITTED,'Submitted for review'),
#         (STATUS_ACCEPTED,'Submission accepted'),
#         (STATUS_RECEIVED,'Samples received'),
#         (STATUS_PASSED_QC,'Samples passed QC'),
#         (STATUS_LIBRARIES_PREPPED,'Libraries prepped'),
#         (STATUS_DATA_AVAILABLE,'Data available')
#         )
    PERMISSION_ADMIN = 'ADMIN'
    PERMISSION_MODIFY = 'MODIFY'
    PERMISSION_VIEW = 'VIEW'
    PAYMENT_DAFIS = 'DaFIS'
    PAYMENT_UC = 'UC Chart String'
    PAYMENT_CREDIT_CARD = 'Credit Card'
    PAYMENT_PO = 'Purchase Order'
    PAYMENT_CHECK = 'Check'
    PAYMENT_WIRE_TRANSFER = 'Wire Transfer'
    PAYMENT_CHOICES = ((PAYMENT_DAFIS,'UCD KFS Account'),(PAYMENT_UC,PAYMENT_UC),(PAYMENT_CREDIT_CARD,PAYMENT_CREDIT_CARD),(PAYMENT_PO,PAYMENT_PO),(PAYMENT_CHECK,PAYMENT_CHECK),(PAYMENT_WIRE_TRANSFER,PAYMENT_WIRE_TRANSFER))
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT, related_name='submissions')
    internal_id = models.CharField(max_length=25, null=True)
    status = models.CharField(max_length=50, null=True)#models.ForeignKey(SubmissionStatus,null=True,on_delete=models.SET_NULL)
    locked = models.BooleanField(default=False)
    cancelled = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    confirmed = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
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
    notes = models.TextField(null=True,blank=True) #Not really being used in interface?  Should be for admins.
    biocore = models.BooleanField(default=False)
    participants = models.ManyToManyField(User,blank=True, related_name='+')
    users = models.ManyToManyField(User,blank=True, related_name="submissions")
    samples_received = models.DateField(null=True, blank=True)
    received_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.PROTECT)
    data = JSONField(default=dict)
    payment = JSONField(default=dict)
    comments = models.TextField(null=True, blank=True)
#     import_url = models.URLField(null=True, blank=True)
    import_internal_id = models.CharField(max_length=25, null=True)
    import_data = JSONField(null=True, blank=True)
    import_request = models.ForeignKey('Import', null=True, blank=True, on_delete=models.SET_NULL, related_name='submissions')
    warnings = JSONField(null=True, blank=True)
    def permissions(self, user):
        if user.is_superuser or self.participants.filter(username=user.username).exists():
            return [Submission.PERMISSION_ADMIN, Submission.PERMISSION_MODIFY, Submission.PERMISSION_VIEW]
        elif self.lab.users.filter(username=user.username).exists():
            return [Submission.PERMISSION_VIEW]
        elif self.users.filter(username=user.username).exists():
            return [Submission.PERMISSION_VIEW] if self.locked else [Submission.PERMISSION_MODIFY, Submission.PERMISSION_VIEW]
        else:
            return []
    @staticmethod
    def get_queryset(institution=None, user=None):
#         return viewsets.ModelViewSet.get_queryset(self).select_related('lab')
        if not user:
            return Submission.objects.none()
        queryset = Submission.objects.filter(lab__institution=institution) if institution else Submission.objects.all()
        if not user.is_superuser:
            queryset = queryset.filter(Q(lab__users__username=user.username)|Q(users__username=user.username)|Q(participants__username=user.username))
        return queryset.select_related('lab').distinct()
#         if lab:
#             queryset = queryset.filter(lab__lab_id=lab)
#             if not user.is_superuser:
#                 queryset = queryset.filter(lab__users__username=user.username)
#         else:
#             queryset = queryset.filter(users__username=user.username)
#         return queryset.select_related('lab').distinct()
#     @staticmethod
#     def user_queryset(self, request=None):
#         from dnaorder.utils import get_site_institution
#         if not request.user:
#             return Submission.objects.none()
#         institution = get_site_institution(self.request)
#         return queryset.filter(lab__institution=institution)
    def save(self, *args, **kwargs):
        self.lab = self.type.lab
        if not self.cancelled and not self.internal_id:
#             prefix, created = PrefixID.objects.get_or_create(prefix=self.type.prefix,lab=self.lab)
            
#             prefix.current_id += 1
            self.internal_id = self.type.get_next_id() #"{0}{1}".format(self.type.prefix, str(self.type.next_id).zfill(4))
            self.type.next_id += 1
            self.type.save()
        if not self.sample_schema:
            self.sample_schema = self.type.sample_schema
        if not self.submission_schema:
            self.submission_schema = self.type.submission_schema
        super(Submission, self).save(*args, **kwargs)
#     def generate_internal_id(self):
#         prefix, created = Prefix.object.get_or_create(prefix=self.type.prefix) 
#         base_id = "{prefix}{date:%y}{date:%m}{date:%d}".format(prefix=prefix,date=self.submitted or timezone.now())
#         for i in range(1,100):#that's a lot of submissions per day!
#             id = '{base_id}_{i}'.format(base_id=base_id,i=i)
#             if not Submission.objects.filter(internal_id=id).exists():
#                 return id
# #         Submission.objects.filter(internal_id__starts_with=base_id).order_by('-internal_id')
    def get_files(self):
        from dnaorder.api.serializers import SubmissionFileSerializer
        return SubmissionFileSerializer(self.files.all(),many=True).data
    def get_lab_from_email(self):
        return "no-reply@{0}".format(self.lab.site.domain)
    def get_participant_emails(self):
        emails = [p.email for p in self.participants.all() if p.email]
        if len(emails) == 0:
            emails = [self.lab.email]
        return emails
    def get_submitter_emails(self):
        emails = [c.email for c in self.contacts.all() if c.email] + [self.email, self.pi_email]
        return emails
    def cancel(self):
        self.cancelled = timezone.now()
        # Try to rescue the id if we haven't moved on yet
        if self.internal_id == self.type.get_previous_id():
            self.type.next_id -= 1
            self.type.save()
        self.internal_id = None
        self.save()
        self.samples.all().delete() #delete associated samples
    def update_samples(self, sample_data):
        print('sample_data', sample_data)
        sample_ids = [s['id'] for s in sample_data if s.get('id',False)]
        #Delete samples that no longer exist
        print('sample_ids',sample_ids)
        Sample.objects.filter(submission=self).exclude(id__in=sample_ids).delete()
        
        #What is the largest current suffix?
        last_sample = Sample.objects.filter(submission=self).order_by('-id_suffix').first()
        suffix = last_sample.id_suffix if last_sample else 0
        
        for i, s in enumerate(sample_data):
            row = i+1
            id = s.get('id',None)
            if not id: #create
                print('CREATING row {}'.format(row), s)
                suffix += 1
                id = "{}_{}".format(self.internal_id,str(suffix).zfill(3))
                s['id'] = id
                sample = Sample.objects.create(id=id, id_suffix=suffix, submission=self, name=s.get('sample_name',''),data=s,row=row)
                print("CREATE {}: id: {}, name: {}".format(row,id,s.get('sample_name','""')))
            else: #update
                sample = Sample.objects.get(submission=self,id=id)
                sample.name = s.get('sample_name','')
                sample.data=s
                sample.row=row
                sample.save()
                print("UPDATE {}: id: {}, name: {}".format(row,id,s.get('sample_name','""')))
    def __str__(self):
        return '{id}: {submitted} - {type} - {pi_first_name} {pi_last_name}'.format(id=self.id,submitted=self.submitted,type=str(self.type),pi_first_name=self.pi_first_name,pi_last_name=self.pi_last_name)
    class Meta:
        ordering = ['submitted']
        unique_together = (('internal_id','lab'))
#     @property
#     def samplesheet(self):
#         from dnaorder.spreadsheets import CoreSampleSheet
#         return CoreSampleSheet(self.sample_form.file,self.type)
#     @property
#     def submission_samplesheet(self):
#         if not self.type.has_submission_fields:
#             return None
#         from dnaorder.spreadsheets import SubmissionData
#         return SubmissionData(self.sample_form.file,self.type)
#     @property
#     def sra_samplesheet(self):
#         from dnaorder.spreadsheets import SRASampleSheet
#         return SRASampleSheet(self.sra_form.file) if self.sra_form else None
    @property
    def sample_ids(self):
        return [s.get(self.type.sample_identifier) for s in self.sample_data]
    def editable(self,user=None):
        if user and (user.is_superuser or self.participants.filter(username=user.username).exists()):
            return True
        return not self.locked
#     def get_user_permissions(self, user):
#         permissions = []
#         if user:
#             if user.is_superuser or self.participants.filter(username=user.username).exists():
#                 permissions.append(Submission.PERMISSION_ADMIN)
#         return permissions
    def get_absolute_url(self, full_url=False):
#         from django.urls import reverse
#         return reverse('submission', args=[str(self.id)])
        return '{}/submissions/{}'.format(settings.BASE_URI if full_url else '', self.id)
#     def set_status(self,status,commit=True):
#         self.status = status
#         if status.auto_lock:
#             self.locked = True
#         if commit:
#             self.save()
    @property
    def participant_emails(self):
        participants = [u.email for u in self.participants.all()]
        if len(participants) == 0:
            if self.type.default_participants.count() > 0:
                participants = [u.email for u in self.type.default_participants.all()]
            else:
                participants = [settings.LAB_EMAIL]
        return participants

@receiver(signals.post_save, sender=Submission)
def set_default_participants(sender, instance, created, **kwargs):
    if created and instance.type.default_participants.count() > 0:
        for u in instance.type.default_participants.all():
            instance.participants.add(u)

class Sample(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    id_suffix = models.PositiveIntegerField()
    row = models.PositiveIntegerField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="samples")
    name = models.CharField(max_length=50,db_index=True)
#     received = models.DateField(null=True,blank=True,db_index=True)
    data = JSONField(null=True,blank=True)
    def __unicode__(self):
        return self.id
    def __str__(self):
        return self.id
#     def get_absolute_url(self):
#         return reverse('sample', args=[str(self.id)])
#     def directory(self,full=True):
#         return call_directory_function('get_sample_directory',self,full=full)
    class Meta:
        unique_together = (('name', 'submission'),('id_suffix','submission'))


class Draft(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    data = JSONField(null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Import(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=25, null=True, blank=True)
    url = models.URLField()
    api_url = models.URLField()
    data = JSONField(null=False,blank=False)

class Contact(models.Model):
    submission = models.ForeignKey(Submission, related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    
class SubmissionFile(models.Model):
    id = models.CharField(max_length=15, primary_key=True, default=generate_file_id, editable=False)
    submission = models.ForeignKey(Submission,related_name="files", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=submission_file_path)
    def get_filename(self):
        return os.path.basename(self.file.name)
    def get_size(self):
        return self.file.size
    def formatted_size(self):
        from django.template.defaultfilters import filesizeformat
        return filesizeformat(self.get_size())
    def get_modified(self):
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.file.file.name))
    def formatted_date(self):
        return self.uploaded_at.strftime('%x %X')
    class Meta:
        ordering = ['id']

# class Validator(models.Model):
#     field_id = models.CharField(max_length=30)
#     message = models.CharField(max_length=250,null=True,blank=True)
#     regex = models.CharField(max_length=250,null=True,blank=True)
#     choices = models.TextField(null=True,blank=True)
#     range = FloatRangeField(null=True,blank=True)
#     def __str__(self):
#         return self.field_id
#     def is_valid(self,value):
#         if self.regex:
#             pattern = re.compile(self.regex)
#             if not pattern.match(str(value)):
#                 return False
#         if self.choices and str(value) not in [c.strip() for c in self.choices.split(',')]:
#             return False
#         if self.range:
#             try:
#                 v = float(value)
#                 if not v in self.range:
#                     return False
#             except:
#                 return False
#         return True

class Note(models.Model):
    TYPE_LOG = 'LOG'
    TYPE_NOTE = 'NOTE'
    TYPES = ((TYPE_LOG,TYPE_LOG),(TYPE_NOTE,TYPE_NOTE))
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    parent = models.ForeignKey('Note',null=True, on_delete=models.PROTECT)
    text = models.TextField()
    type = models.CharField(max_length=20,choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.PROTECT)
    emails = ArrayField(models.CharField(max_length=50),blank=True,null=True)
    sent = models.NullBooleanField()
    public = models.BooleanField(default=False)
    class Meta:
        ordering = ['id']
    def can_modify(self,user):
        return not user.is_anonymous and self.type == Note.TYPE_NOTE and self.created_by == user# or not self.created_by
@receiver(signals.post_save, sender=Note)
def send_note_email(sender, instance, created, **kwargs):
#     'Note created'
    if created and instance.emails:
        emails.note_email(instance)
        instance.sent = True
        instance.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    settings = JSONField(default=dict)

class UserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField() # must be validated before entry
    validated = models.DateTimeField(null=True)

def user_string(self):
    if self.first_name or self.last_name:
        return "{first} {last}".format(first=self.first_name, last=self.last_name)
    else:
        return self.username
User.__str__ = user_string
User.__str__ = user_string

@receiver(signals.post_save, sender=User)
def user_created_assign_submissions(sender, instance, created, **kwargs):
    from dnaorder.utils import assign_submissions
    if instance.email: #May want to put this as a hook on a "validated email" model instead.
        assign_submissions(instance)

class Vocabulary(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=50)

class Term(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    obj = JSONField(null=True, blank=True)
    class Meta:
        ordering = ['vocabulary', 'value']
        unique_together = (('vocabulary','value'),)