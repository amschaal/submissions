from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.fields.jsonb import JSONField
from django.forms.fields import RegexField
import re

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
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'submissions/{date:%Y}/{date:%m}/{date:%d}/{order_id}/{filename}'.format(date=timezone.now(),order_id=instance.id,filename=filename)
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
def sample_form_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'submissions/{date:%Y}/{date:%m}/{date:%d}/{order_id}/{filename}'.format(date=timezone.now(),order_id=instance.id,filename=filename)

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    def __unicode__(self):
        return '{submitted} - {type} - {pi}'.format(submitted=self.submitted,type=str(self.type),pi=self.pi_name)
    class Meta:
        ordering = ['submitted']

class Validator(models.Model):
    field_id = models.CharField(max_length=30)
    message = models.CharField(max_length=250,null=True,blank=True)
    regex = models.CharField(max_length=250,null=True,blank=True)
    choices = models.TextField(null=True,blank=True)
    def is_valid(self,value):
        if self.regex:
            pattern = re.compile(self.regex)
            if not pattern.match(str(value)):
                return False
            
