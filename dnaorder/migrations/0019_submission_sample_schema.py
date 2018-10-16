# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-28 22:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0018_submissiontype_help'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='sample_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
