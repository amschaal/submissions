# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-07 22:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0008_auto_20180507_2116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submissiontype',
            old_name='submission_header_index',
            new_name='submission_header_row',
        ),
        migrations.RenameField(
            model_name='submissiontype',
            old_name='submission_skip_rows',
            new_name='submission_value_row',
        ),
    ]