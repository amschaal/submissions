from rest_framework import filters
from django.contrib.auth.models import User

from schema.utils import all_submission_type_filters
class ParticipatingFilter(filters.BaseFilterBackend):
    """
    Only show submissions in which the user is a participant
    """
    def filter_queryset(self, request, queryset, view):
        participating = view.request.query_params.get('participating',None)
        if participating is not None:
            return queryset.filter(participants__in=[request.user])
        else:
            return queryset
class MySubmissionsFilter(filters.BaseFilterBackend):
    """
    Only show submissions in which the user is a submitter or PI
    """
    def filter_queryset(self, request, queryset, view):
        my_submissions = view.request.query_params.get('my_submissions',None)
        if my_submissions is not None:
            return queryset.filter(users__in=[request.user])
        else:
            return queryset

class ExcludeStatusFilter(filters.BaseFilterBackend):
    """
    Exclude submissions based on status
    """
    def filter_queryset(self, request, queryset, view):
        exclude_status = view.request.query_params.get('exclude_status',None)
        if exclude_status is not None:
            return queryset.exclude(status__iexact=exclude_status)
        else:
            return queryset

class hasSubmissions(filters.BaseFilterBackend):
    """
    Exclude submissions based on status
    """
    def filter_queryset(self, request, queryset, view):
        has_submissions = view.request.query_params.get('has_submissions',None)
        if has_submissions:
            return queryset
        else:
            return queryset.filter(submissions__id__isnull=True)

class LabFilter(filters.BaseFilterBackend):
    """
    Make consistent lab=<lab_id> query parameter
    """
    def filter_queryset(self, request, queryset, view):
        lab = view.request.query_params.get('lab', None)
        lab_filter = getattr(view, 'lab_filter', None) # e.g. lab_query = 'lab__lab_id'
        if lab and lab_filter:
            return queryset.filter(**{lab_filter: lab})
        else:
            return queryset
        
class UserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        lab = view.request.query_params.get('lab', None)
        if not lab:
            return queryset
        users = User.objects.filter(lab_permissions__permission_object__lab_id=lab)
        return queryset.distinct() & users.distinct()

class JSONFilter(filters.BaseFilterBackend):
    """
    Allow generic filtering of configured JSONFields
    ex: &submission_data__libraries__i5__contains=GTACTCTC&&submission_data__pools__quantification__contains=Qubit&submission_data__pools__libkit__contains=NEB&submission_data__custom_primers__icontains=Illumina&submission_data__index_desc=Dual&submission_data__demux=Yes
    """
    def filter_queryset(self, request, queryset, view):
        filter_fields = getattr(view,'json_filter_fields',[])
        for q, v in view.request.query_params.items():
            parts = q.split('__')
            if parts[0] in filter_fields:
                if parts[-1] == 'contains': # This is used for filtering lists.  We can only filter exact values, and the format is path__to__list__contains=[{key:value}]
                    field = parts.pop(-2) # Remove the field name to add as key to [{key:value}] lookup
                    v = [{field: v}]
                    q = '__'.join(parts) # Create the filter lookup, which is the original query param, with the field name removed (and added to lookup)
                elif parts[-1] == 'boolean': # Will need to convert value from string to Python True or False
                    parts.pop() # Remove the boolean filter.  This is an exact match, we are just cleaning the data.
                    if v in ['true', 'True', 1, '1']:
                        v = True
                    elif v in ['false', 'False', 0, '0']:
                        v = False
                    q = '__'.join(parts)
                queryset = queryset.filter(**{q:v})
        return queryset

def get_lab_filters(lab):
    filters = {'type': all_submission_type_filters(lab)}
    # {'id':['icontains','exact'],'internal_id':['icontains','exact'],'import_internal_id':['icontains','exact'],'phone':['icontains'],'first_name':['icontains'],'last_name':['icontains'],'email':['icontains'],'pi_first_name':['icontains'],'pi_last_name':['icontains'],'pi_email':['icontains'],'institute':['icontains'],'type__name':['icontains'],'status':['icontains','iexact'],'biocore':['exact'],'locked':['exact'],'type':['exact'],'cancelled':['isnull']}
    filters['general'] = {
            'id': { "type": "string", "title": "System ID (random string)", "filters": [{"label": "=", "filter": "id"}, {"label": "contains", "filter": "id__icontains"}]},
            'internal_id': { "type": "string", "title": "Project ID", "filters": [{"label": "=", "filter": "internal_id"}, {"label": "contains", "filter": "internal_id__icontains"}, {"label": "starts with", "filter": "internal_id__istartswith"}]},
            'status': { "type": "string", "title": "Status", "enum": lab.statuses, "filters": [{"label": "=", "filter": "status__iexact"}]},
            'email': { "type": "string", "title": "Submitter email", "filters": [{"label": "contains", "filter": "email__icontains"}]},
            'pi_email': { "type": "string", "title": "PI email", "filters": [{"label": "contains", "filter": "pi_email__icontains"}]},
            'biocore': { "type": "boolean", "title": "Biocore", "enum": ['True', 'False'], "filters": [{"label": "=", "filter": "biocore"}]},
            'locked': { "type": "boolean", "title": "Locked", "enum": ['True', 'False'], "filters": [{"label": "=", "filter": "locked"}]},
            'submitted__date': { "type": "date", "title": "Submission Date", "filters": [{"label": "=", "filter": "submitted__date"}, {"label": ">=", "filter": "submitted__date__gte"}, {"label": "<=", "filter": "submitted__date__lte"}]},
            'samples_received__date': { "type": "date", "title": "Samples received date", "filters": [{"label": "=", "filter": "samples_received"}, {"label": ">=", "filter": "samples_received__gte"}, {"label": "<=", "filter": "samples_received__lte"}]},
            'samples_received': { "type": "boolean", "title": "Samples not received", "enum": ['True', 'False'], "filters": [{"label": "=", "filter": "samples_received__isnull"}]},
            # 'cancelled': { "type": "boolean", "title": "Cancelled", "enum": ['True', 'False'], "filters": [{"label": "=", "filter": "cancelled__isnull"}]}
        }
    return filters