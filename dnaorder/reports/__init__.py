from collections import OrderedDict
from django.db.models.functions import Trunc
from django.db.models import Count, DateTimeField, QuerySet
REPORTS = OrderedDict()

class BaseReport:
    PERIOD_MONTH = 'month'
    PERIOD_YEAR = 'year'
    PERIOD_QUARTER = 'quarter'
    ID = None
    NAME = None
    DESCRIPTION = None
    @staticmethod
    def get_data(queryset: QuerySet) -> list[dict]:
        raise NotImplementedError
    @staticmethod
    def get_headers(queryset: QuerySet) -> dict:
        raise NotImplementedError
    @classmethod
    def serialize(cls) -> dict:
        return { 'id': cls.ID, 'name': cls.NAME, 'description': cls.DESCRIPTION }
    @staticmethod
    def annotate_period(queryset: QuerySet, period: str) -> QuerySet:
        if period == BaseReport.PERIOD_MONTH:
           return BaseReport.annotate_month(queryset)
        elif period == BaseReport.PERIOD_YEAR:
            return BaseReport.annotate_year(queryset)
        elif period == BaseReport.PERIOD_QUARTER:
            return BaseReport.annotate_quarter(queryset)
    @staticmethod
    def annotate_month(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(month=Trunc("submitted", BaseReport.PERIOD_MONTH, output_field=DateTimeField()))
    @staticmethod
    def annotate_year(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(year=Trunc("submitted", BaseReport.PERIOD_YEAR, output_field=DateTimeField()))
    @staticmethod
    def annotate_quarter(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(quarter=Trunc("submitted", BaseReport.PERIOD_QUARTER, output_field=DateTimeField()))

class FieldReport(BaseReport):
    FIELDS = []
    ORDER_BY = []
    @staticmethod
    def get_headers(period) -> dict:
        return {
            "type__name": "Submission Type",
            "count": 'Number of Submissions'
        }
    @classmethod
    def get_fields(cls) -> list:
        return cls.FIELDS
    @classmethod
    def get_order(cls) -> list:
        return cls.ORDER_BY
    @classmethod
    def annotate(cls, queryset: QuerySet) -> QuerySet:
        return queryset
    @classmethod
    def get_data(cls, queryset, period=BaseReport.PERIOD_MONTH):
        fields = cls.get_fields()
        order = cls.get_order()
        if period:
            queryset = BaseReport.annotate_period(queryset, period).values(*fields, period).order_by(period, *order)
        else:
            queryset = queryset.values(*fields).order_by(*order)
        return cls.annotate(queryset)