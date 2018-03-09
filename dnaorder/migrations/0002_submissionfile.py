# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-08 19:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import dnaorder.models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=dnaorder.models.submission_file_path)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnaorder.Submission')),
            ],
        ),
    ]
