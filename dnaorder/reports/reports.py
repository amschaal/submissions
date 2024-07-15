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
    def get_headers(period=BaseReport.PERIOD_MONTH) -> dict:
        return {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            period: 'Period'
        }
    def get_data(queryset, period=BaseReport.PERIOD_MONTH):
        if period:
            queryset = BaseReport.annotate_period(queryset, period)
            return queryset.values('type__name', period).order_by(period, 'type__name').annotate(count=Count('type__name'))
        return queryset.values('type__name').order_by('type__name').annotate(count=Count('type__name'))

register_report(SubmissionTypeCountReport)

class SubmissionTypeCountReport2(FieldReport):
    ID = 'SubmissionTypeCount2'
    NAME = 'Submission Type Count2'
    DESCRIPTION = 'Get the number of submissions by type'
    FIELDS = ['type__name']
    ORDER_BY = ['type__name']
    @staticmethod
    def get_headers(period=BaseReport.PERIOD_MONTH) -> dict:
        return {
            'type__name': 'Submission Type',
            'count': 'Number of Submissions',
            period: 'Period'
        }
    @classmethod
    def annotate(cls, queryset):
        return queryset.annotate(count=Count('type__name'))
register_report(SubmissionTypeCountReport2)