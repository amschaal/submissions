# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from dnaorder.models import Lab, Submission

class Service(models.Model):
    lab = models.ForeignKey(Lab)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return '{0}: {1} - {2}'.format(self.lab.name, self.code, self.name)
    class Meta:
        unique_together = (('lab','code'), ('lab','name'))

class LineItem(models.Model):
    submission = models.ForeignKey(Submission, related_name="line_items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.FloatField()
    notes = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)