import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import dnaorder.models
import dnaorder.storage


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0019_payment_required'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LabFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(max_length=255, storage=dnaorder.storage.ProtectedStorage(), upload_to=dnaorder.models.lab_file_path)),
                ('internal', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='dnaorder.lab')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['lab', 'name'],
            },
        ),
    ]
