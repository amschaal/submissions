from django.db import models
import uuid
from django.utils import timezone

class SubmissionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    form = models.FileField(upload_to='submission_forms/')
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
    sra_form = models.FileField(upload_to=sra_samples_path)
    def __unicode__(self):
        return '{submitted} - {type} - {pi}'.format(submitted=self.submitted,type=str(self.type),pi=self.pi_name)

    
    