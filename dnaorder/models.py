from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.fields.jsonb import JSONField
from django.forms.fields import RegexField
import re
import os
from django.contrib.postgres.fields.ranges import FloatRangeField
import datetime
from dnaorder.fields import EmailListField, EmailArrayField
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from dnaorder import emails
from django.contrib.postgres.fields.array import ArrayField
from django.db.models.signals import post_save
from django.template.defaultfilters import default

def default_schema():
    return {'properties': {}, 'order': [], 'required': [], 'layout': {}}

class SubmissionType(models.Model):
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,null=True,blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    prefix = models.CharField(max_length=15,null=True,blank=True)
    sample_identifier = models.CharField(max_length=25,default='sample_name')
    exclude_fields = models.TextField(blank=True)
    submission_help = models.TextField(null=True,blank=True)
    submission_schema = JSONField(null=True,default=default_schema)
    sample_schema = JSONField(null=True,default=default_schema)
    examples = JSONField(default=list)
    sample_help = models.TextField(null=True,blank=True)
    def __unicode__(self):
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

class SubmissionStatus(models.Model):
    order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=40)
    auto_lock = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Submission Statuses"
        ordering = ['order']

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
    PAYMENT_DAFIS = 'DaFIS'
    PAYMENT_UC = 'UC Chart String'
    PAYMENT_CREDIT_CARD = 'Credit Card'
    PAYMENT_PO = 'Purchase Order'
    PAYMENT_CHECK = 'Check'
    PAYMENT_WIRE_TRANSFER = 'Wire Transfer'
    PAYMENT_CHOICES = ((PAYMENT_DAFIS,'DaFIS (UC Davis Account String)'),(PAYMENT_UC,PAYMENT_UC),(PAYMENT_CREDIT_CARD,PAYMENT_CREDIT_CARD),(PAYMENT_PO,PAYMENT_PO),(PAYMENT_CHECK,PAYMENT_CHECK),(PAYMENT_WIRE_TRANSFER,PAYMENT_WIRE_TRANSFER))
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    internal_id = models.CharField(max_length=25, unique=True)
    status = models.ForeignKey(SubmissionStatus,null=True,on_delete=models.SET_NULL)
    locked = models.BooleanField(default=False)
    cancelled = models.DateTimeField(null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20)
    pi_name = models.CharField(max_length=50)
    pi_email = models.EmailField(max_length=75)
    institute = models.CharField(max_length=75)
    payment_type = models.CharField(max_length=50,choices=PAYMENT_CHOICES)
    payment_info = models.CharField(max_length=250,null=True,blank=True)
    type = models.ForeignKey(SubmissionType,related_name="submissions", on_delete=models.PROTECT)
    submission_schema = JSONField(null=True,blank=True)
    sample_schema = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    sample_data = JSONField(null=True,blank=True)
    sra_data = JSONField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    biocore = models.BooleanField(default=False)
    participants = models.ManyToManyField(User,blank=True)
    data = JSONField(default=dict)
    def save(self, *args, **kwargs):
        if not self.internal_id:
            self.internal_id = self.generate_internal_id()
        if not self.sample_schema:
            self.sample_schema = self.type.sample_schema
        if not self.submission_schema:
            self.submission_schema = self.type.submission_schema
        super(Submission, self).save(*args, **kwargs)
    def generate_internal_id(self):
        prefix = self.type.prefix or ''
        print prefix
        base_id = "{prefix}{date:%y}{date:%m}{date:%d}".format(prefix=prefix,date=self.submitted or timezone.now())
        for i in range(1,100):#that's a lot of submissions per day!
            id = '{base_id}_{i}'.format(base_id=base_id,i=i)
            if not Submission.objects.filter(internal_id=id).exists():
                return id
#         Submission.objects.filter(internal_id__starts_with=base_id).order_by('-internal_id')
    def get_files(self):
        from dnaorder.api.serializers import SubmissionFileSerializer
        return SubmissionFileSerializer(self.files.all(),many=True).data
    def __unicode__(self):
        return '{id}: {submitted} - {type} - {pi}'.format(id=self.id,submitted=self.submitted,type=str(self.type),pi=self.pi_name)
    class Meta:
        ordering = ['submitted']
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
        if user and user.is_authenticated:
            return True
        return not self.locked
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission', args=[str(self.id)])
    def set_status(self,status,commit=True):
        self.status = status
        if status.auto_lock:
            self.locked = True
        if commit:
            self.save()
    @property
    def participant_emails(self):
        participants = [u.email for u in self.participants.all()]
        if len(participants) == 0:
            participants = ['dnatech@ucdavis.edu']
        return participants

class Contact(models.Model):
    submission = models.ForeignKey(Submission, related_name='contacts')
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    
class SubmissionFile(models.Model):
    id = models.CharField(max_length=15, primary_key=True, default=generate_file_id, editable=False)
    submission = models.ForeignKey(Submission,related_name="files")
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
#     def __unicode__(self):
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
    submission = models.ForeignKey(Submission)
    parent = models.ForeignKey('Note',null=True)
    text = models.TextField()
    type = models.CharField(max_length=20,choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,null=True)
    emails = ArrayField(models.CharField(max_length=50),blank=True,null=True)
    sent = models.NullBooleanField()
    public = models.BooleanField(default=False)
    class Meta:
        ordering = ['id']
    def can_modify(self,user):
        return not user.is_anonymous and self.type == Note.TYPE_NOTE and self.created_by == user# or not self.created_by
@receiver(signals.post_save, sender=Note)
def send_note_email(sender, instance, created, **kwargs):
    'Note created'
    if created and instance.emails:
        print instance.emails
        emails.note_email(instance)
        instance.sent = True
        instance.save()

def user_string(self):
    if self.first_name or self.last_name:
        return "{first} {last}".format(first=self.first_name, last=self.last_name)
    else:
        return self.username
User.__unicode__ = user_string
User.__str__ = user_string