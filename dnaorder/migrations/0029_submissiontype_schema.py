# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-01 17:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0028_auto_20181031_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True),
        ),
    ]
