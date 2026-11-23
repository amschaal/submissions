import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0021_submissionfile_field_uploads'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drafts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(django.db.models.functions.text.Lower('email'), name='submission_email_lower'),
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(django.db.models.functions.text.Lower('pi_email'), name='submission_pi_email_lower'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(django.db.models.functions.text.Lower('email'), name='contact_email_lower'),
        ),
    ]
