import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import dnaorder.models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0020_labfile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionfile',
            name='submission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='dnaorder.submission'),
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='file',
            field=models.FileField(max_length=255, upload_to=dnaorder.models.submission_file_path),
        ),
        migrations.AddField(
            model_name='submissionfile',
            name='variable',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='submissionfile',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
