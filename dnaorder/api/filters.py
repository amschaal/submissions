from rest_framework import filters
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