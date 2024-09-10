from dnaorder.reports import BaseReport, REPORTS, FieldReport
from django.db.models.aggregates import Count

def register_report(Report):
    REPORTS[Report.ID] = Report

def get_report_by_id(id):
    return REPORTS[id]

def list_reports():
    return [ r.serialize() for r in REPORTS.values() ]

class SubmissionTypeCountReport(BaseReport):
    ID = 'SubmissionTypeCount'
    NAME = 'Submission Type Count'
    DESCRIPTION = 'Get the number of submissions by type'
    @staticmethod
    def get_headers(period=BaseReport.PERIOD_MONTH, lab_id=None) -> dict:
        return {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            'period': period
        }
    def get_data(queryset, period=BaseReport.PERIOD_MONTH, lab_id=None):
        if period:
            queryset = BaseReport.annotate_period(queryset, period)
            return queryset.values('type__name', 'period').order_by('period', 'type__name').annotate(count=Count('type__name'))
        return queryset.values('type__name').order_by('type__name').annotate(count=Count('type__name'))

register_report(SubmissionTypeCountReport)


class SubmissionStatusReport(BaseReport):
    ID = 'SubmissionStatus'
    NAME = 'Submission Status Report'
    DESCRIPTION = 'Get the amount of time submissions spend within each status'
    def get_statuses(lab_id):
        from dnaorder.models import Lab
        lab = Lab.objects.filter(lab_id=lab_id).first()
        return lab.statuses if lab else []
    @staticmethod
    def get_headers(period=BaseReport.PERIOD_MONTH, lab_id=None) -> dict:
        statuses = SubmissionStatusReport.get_statuses(lab_id)
        status_headers = ['STATUS_{}'.format(s).replace(' ','_') for s in statuses]
        headers = {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            'period': period
        }
        for h in status_headers:
            headers[h] = h
        return headers
    def get_data(queryset, period=BaseReport.PERIOD_MONTH, lab_id=None):
        from django.db.models import Count, F, Sum, Avg, FloatField, IntegerField, Max, Min
        from django.db.models.functions import Cast
        # queryset = queryset.filter(data__status_durations__isnull=False)
        statuses = SubmissionStatusReport.get_statuses(lab_id)
        annotations = {'STATUS_{}'.format(s).replace(' ','_') : Cast(Avg(Cast(F("data__status_durations__{}".format(s)), output_field=FloatField())), IntegerField()) for s in statuses}
        # raise Exception(annotations)
        if period:
            values = ['type__name', 'period']#+['STATUS_{}'.format(s).replace(' ','_') for s in statuses]
            queryset = BaseReport.annotate_period(queryset, period)
            return queryset.values(*values).order_by(*values).annotate(**annotations)
        values = ['type__name']#+['STATUS_{}'.format(s).replace(' ','_') for s in statuses]
        return queryset.values(*values).order_by(*values).annotate(**annotations)
"""
Update status stats based on logs:
from dnaorder.models import *
import re
re_text = 'Submission status updated to "(.+)"'
def update_status_stats(max=100):
    for s in Submission.objects.filter(data__status_updates__isnull=True)[:max]:
        s.data['status_updates'] = []
        s.data['status_durations'] = {}
        s.save(update_fields=['data'])
        for n in s.note_set.filter(text__contains='Submission status updated').order_by('created'):
            matches = re.findall(re_text, n.text)
            if len(matches) == 1:
                print('update status', matches[0], n.created)
                s.add_status_update(matches[0], n.created, save=True)
"""


register_report(SubmissionStatusReport)
# Submission.objects.filter(data__status_durations__isnull=False).annotate(status_data=F("data__status_durations__Samples Received"))

class SubmissionTypeCountReport2(FieldReport):
    ID = 'SubmissionTypeCount2'
    NAME = 'Submission Type Count2'
    DESCRIPTION = 'Get the number of submissions by type'
    PERIODS = None
    FIELDS = ['type__name']
    ORDER_BY = ['type__name']
    @staticmethod
    def get_headers(period=BaseReport.PERIOD_MONTH, lab_id=None) -> dict:
        return {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            'period': period
        }
    @classmethod
    def annotate(cls, queryset):
        return queryset.annotate(count=Count('type__name'))
# register_report(SubmissionTypeCountReport2)