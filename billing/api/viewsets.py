from rest_framework import viewsets, response, status
from billing.models import Service, LineItem
from billing.api.serializers import ServiceSerializer, LineItemSerializer
from rest_framework.permissions import AllowAny
from billing.api.permissions import LineItemPermissions

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    filter_fields = {'name':['icontains'],'lab':['exact'],'code':['exact','icontains']}
    search_fields = ('name','code','description')
    queryset = Service.objects.filter(enabled=True).order_by('code')
    serializer_class = ServiceSerializer
    ordering_fields = ['name','code']
    permission_classes = (AllowAny,)

class LineItemViewSet(viewsets.ModelViewSet):
    filter_fields = {'submission':['exact']}
    queryset = LineItem.objects.all().order_by('service__code')
    serializer_class = LineItemSerializer
    ordering_fields = ['service__name','service__code']
    permission_classes = (LineItemPermissions,)