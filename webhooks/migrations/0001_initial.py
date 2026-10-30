import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dnaorder', '0019_payment_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True)),
                ('url', models.URLField(blank=True, max_length=500)),
                ('auth_header', models.CharField(default='Authorization', max_length=100)),
                ('encrypted_secret', models.TextField(blank=True, editable=False)),
                ('last_sent', models.DateTimeField(editable=False, null=True)),
                ('last_status', models.IntegerField(editable=False, null=True)),
                ('last_error', models.CharField(blank=True, editable=False, max_length=250)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhooks', to='dnaorder.lab')),
                ('submission_type', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webhook', to='dnaorder.submissiontype')),
            ],
            options={
                'constraints': [models.UniqueConstraint(condition=models.Q(('submission_type', None)), fields=('lab',), name='webhook_one_default_per_lab')],
            },
        ),
    ]
