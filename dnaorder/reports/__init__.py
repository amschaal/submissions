from collections import OrderedDict
from django.db.models.functions import Trunc
from django.db.models import Count, DateTimeField
REPORTS = OrderedDict()

class BaseReport:
    PERIOD_MONTH = 'month'
    PERIOD_YEAR = 'year'
    PERIOD_QUARTER = 'quarter'
    ID = None
    NAME = None
    DESCRIPTION = None
    @staticmethod
    def get_data(queryset):
        raise NotImplementedError
    @classmethod
    def serialize(cls):
        return { 'id': cls.ID, 'name': cls.NAME, 'description': cls.DESCRIPTION }
    @staticmethod
    def annotate_month(queryset):
        return queryset.annotate(month=Trunc("submitted", 'month', output_field=DateTimeField()))
    @staticmethod
    def annotate_year(queryset):
        return queryset.annotate(year=Trunc("submitted", 'year', output_field=DateTimeField()))
    @staticmethod
    def annotate_quarter(queryset):
        return queryset.annotate(quarter=Trunc("submitted", 'quarter', output_field=DateTimeField()))

