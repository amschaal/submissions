from rest_framework import filters
class ParticipatingFilter(filters.BaseFilterBackend):
    """
    Only show submissions in which the user is a participant
    """
    def filter_queryset(self, request, queryset, view):
        participating = view.request.query_params.get('participating',None)
        print 'participating'
        print participating
        if participating is not None:
            return queryset.filter(participants__in=[request.user])
        else:
            return queryset