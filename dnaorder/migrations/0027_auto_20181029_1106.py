# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-29 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0026_auto_20181029_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='first_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]