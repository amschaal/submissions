from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.fields.jsonb import JSONField
from django.forms.fields import RegexField
import re
import os
from django.contrib.postgres.fields.ranges import FloatRangeField
import datetime
from dnaorder.fields import EmailListField
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from dnaorder import emails

class SubmissionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    prefix = models.CharField(max_length=15,null=True,blank=True)
    form = models.FileField(upload_to='submission_forms/')
    header_index = models.PositiveSmallIntegerField(null=True,blank=True,default=0)
    skip_rows = models.PositiveSmallIntegerField(null=True,blank=True,default=1)
    start_column = models.PositiveSmallIntegerField(null=True,blank=True,default=0)
    end_column = models.PositiveSmallIntegerField(null=True,blank=True)
    sample_identifier = models.CharField(max_length=25,default='sample_name')
    def __unicode__(self):
        return self.name

def sra_samples_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = '%s.sra%s'%(instance.id,ext)
    return 'submissions/{date:%Y}/{date:%m}/{submission_id}/{filename}'.format(date=timezone.now(),submission_id=instance.id,filename=filename)
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
def sample_form_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = '%s.samples%s'%(instance.id,ext)
    return 'submissions/{date:%Y}/{date:%m}/{submission_id}/{filename}'.format(date=timezone.now(),submission_id=instance.id,filename=filename)

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
    default = models.BooleanField(default=False)
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
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    internal_id = models.CharField(max_length=25, unique=True)
    status = models.ForeignKey(SubmissionStatus,null=True)
    submitted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20)
    pi_name = models.CharField(max_length=50)
    pi_email = models.EmailField(max_length=75)
    institute = models.CharField(max_length=75)
    type = models.ForeignKey(SubmissionType)
    sample_form = models.FileField(upload_to=sample_form_path)
    sample_data = JSONField(null=True,blank=True)
    sra_form = models.FileField(upload_to=sra_samples_path,null=True,blank=True)
    sra_data = JSONField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    biocore = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.internal_id:
            self.internal_id = self.generate_internal_id()
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
        return '{submitted} - {type} - {pi}'.format(submitted=self.submitted,type=str(self.type),pi=self.pi_name)
    class Meta:
        ordering = ['submitted']
    @property
    def samplesheet(self):
        from dnaorder.spreadsheets import CoreSampleSheet
        return CoreSampleSheet(self.sample_form.file,self.type)
    @property
    def sra_samplesheet(self):
        from dnaorder.spreadsheets import SRASampleSheet
        return SRASampleSheet(self.sra_form.file) if self.sra_form else None
    @property
    def sample_ids(self):
        return [s.get(self.type.sample_identifier) for s in self.sample_data]
    def editable(self,user=None):
        if user and user.is_authenticated:
            return True
        return True if not self.status or self.status.default else False
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission', args=[str(self.id)])

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

class Validator(models.Model):
    field_id = models.CharField(max_length=30)
    message = models.CharField(max_length=250,null=True,blank=True)
    regex = models.CharField(max_length=250,null=True,blank=True)
    choices = models.TextField(null=True,blank=True)
    range = FloatRangeField(null=True,blank=True)
    def __unicode__(self):
        return self.field_id
    def is_valid(self,value):
        if self.regex:
            pattern = re.compile(self.regex)
            if not pattern.match(str(value)):
                return False
        if self.choices and str(value) not in [c.strip() for c in self.choices.split(',')]:
            return False
        if self.range:
            try:
                v = float(value)
                if not v in self.range:
                    return False
            except:
                return False
        return True

class Note(models.Model):
    TYPE_LOG = 'LOG'
    TYPE_NOTE = 'NOTE'
    TYPES = ((TYPE_LOG,TYPE_LOG),(TYPE_NOTE,TYPE_NOTE))
    submission = models.ForeignKey(Submission)
    text = models.TextField()
    type = models.CharField(max_length=20,choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    emails = EmailListField(max_length=200,null=True)
    sent = models.NullBooleanField()
    public = models.BooleanField(default=False)
    class Meta:
        ordering = ['id']
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
User.__str__ = user_string