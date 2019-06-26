# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-14 22:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0032_submissiontype_submission_help'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Validator',
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='sample_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
