# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-04 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]