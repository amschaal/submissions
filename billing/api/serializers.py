from rest_framework import serializers
from billing.models import Service, LineItem
from dnaorder.api.serializers import ModelRelatedField

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = []

class LineItemSerializer(serializers.ModelSerializer):
    service = ModelRelatedField(model=Service,serializer=ServiceSerializer,required=True,allow_null=False)
    class Meta:
        model = LineItem
        exclude = []