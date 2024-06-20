from collections import OrderedDict

REPORTS = OrderedDict()

class BaseReport:
    ID = None
    NAME = None
    DESCRIPTION = None
    @staticmethod
    def get_data(queryset):
        raise NotImplementedError
    @classmethod
    def serialize(cls):
        return { 'id': cls.ID, 'name': cls.NAME, 'description': cls.DESCRIPTION }