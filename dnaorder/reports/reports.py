from dnaorder.reports import BaseReport, REPORTS
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
    def get_data(queryset):
        queryset = queryset.values('type__name').annotate(count=Count('type__name')).order_by('type__name')

register_report(SubmissionTypeCountReport)