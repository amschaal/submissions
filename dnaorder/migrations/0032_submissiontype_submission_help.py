# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-05 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0031_auto_20181205_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='submission_help',
            field=models.TextField(blank=True, null=True),
        ),
    ]
