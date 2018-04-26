# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-25 23:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0006_submission_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='exclude_fields',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='participants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
