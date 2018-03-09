from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.fields.jsonb import JSONField
from django.forms.fields import RegexField
import re
import os
from django.contrib.postgres.fields.ranges import FloatRangeField

class SubmissionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
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
    return 'submissions/{date:%Y}/{date:%m}/{order_id}/{filename}'.format(date=timezone.now(),order_id=instance.id,filename=filename)
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
def sample_form_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = '%s.samples%s'%(instance.id,ext)
    return 'submissions/{date:%Y}/{date:%m}/{order_id}/{filename}'.format(date=timezone.now(),order_id=instance.id,filename=filename)

def submission_file_path(instance, filename):
    return 'submissions/{date:%Y}/{date:%m}/{order_id}/{filename}'.format(date=instance.submission.submitted,order_id=instance.submission.id,filename=filename)

def generate_id():
    while True:
        id = str(uuid.uuid4())[-12:]
        if not Submission.objects.filter(id=id).exists():
            return id
class Submission(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_id, editable=False)
    submitted = models.DateTimeField(auto_now_add=True)
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

class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission,related_name="files")
    file = models.FileField(upload_to=submission_file_path)
    def get_filename(self):
        return os.path.basename(self.file.name)
    def get_size(self):
        return self.file.size
    class Meta:
        ordering = ['-id']

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
            
