from rest_framework import viewsets, response, status
from billing.models import Service, LineItem
from billing.api.serializers import ServiceSerializer, LineItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from billing.api.permissions import LineItemPermissions
from dnaorder.models import Submission

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    filter_fields = {'name':['icontains'],'lab':['exact'],'code':['exact','icontains']}
    search_fields = ('name','code','description')
    queryset = Service.objects.filter(enabled=True).order_by('code')
    serializer_class = ServiceSerializer
    ordering_fields = ['name','code']
    permission_classes = (AllowAny,)

class LineItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = LineItem.objects.all().order_by('service__code')
        submission = self.request.query_params.get('submission',None)
        if submission:
            submission = Submission.objects.filter(id=submission).first()
        if not submission:
            raise PermissionDenied('Must provide a submission id in the request.')
        return queryset.filter(submission=submission)
    queryset = LineItem.objects.all().order_by('service__code')
    serializer_class = LineItemSerializer
    ordering_fields = ['service__name','service__code']
    permission_classes = (LineItemPermissions,)