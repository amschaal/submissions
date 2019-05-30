# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-30 22:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0052_submission_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='home_page',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lab',
            name='payment_type_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='lab',
            name='site',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]
