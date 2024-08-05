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
    def get_data(queryset, period=BaseReport.PERIOD_MONTH, lab_id=None):
        from django.db.models import Count, F, Sum
        queryset = queryset.filter(data__status_durations__isnull=False)
        statuses = SubmissionStatusReport.get_statuses(lab_id)
        annotations = {'STATUS_{}'.format(s).replace(' ','_') : F("data__status_durations__{}".format(s)) for s in statuses}
        # raise Exception(annotations)
        if period:
            values = ['type__name', 'period']+['STATUS_{}'.format(s).replace(' ','_') for s in statuses]
            queryset = BaseReport.annotate_period(queryset, period)
            return queryset.order_by('period', 'type__name').annotate(**annotations).values(*values)
        values = ['type__name']+['STATUS_{}'.format(s).replace(' ','_') for s in statuses]
        return queryset.order_by('type__name').annotate(**annotations).values(*values)

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
    def get_headers(period=BaseReport.PERIOD_MONTH) -> dict:
        return {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            'period': period
        }
    @classmethod
    def annotate(cls, queryset):
        return queryset.annotate(count=Count('type__name'))
register_report(SubmissionTypeCountReport2)