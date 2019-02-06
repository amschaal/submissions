from rest_framework import serializers
from billing.models import Service, LineItem
from dnaorder.api.serializers import ModelRelatedField

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = []

class LineItemSerializer(serializers.ModelSerializer):
#     service = ServiceSerializer()
    service = ModelRelatedField(model=Service,serializer=ServiceSerializer,required=True,allow_null=False)
    class Meta:
        model = LineItem
        exclude = []
#     def __init__(self, *args, **kwargs):
#         
#         service = kwargs.get('data',{}).get('service')
#         if service.get('id'):
#             kwargs['data']['service'] = service.get('id')
#         print args
#         print kwargs
#         return super(LineItemSerializer, self).__init__(*args, **kwargs)
        
#     def create(self, validated_data):
#         validated_data['service'] = validated_data.get('service', {}).get('id')
#         print 'create'
#         print validated_data
#         return LineItem.objects.create(**validated_data)
#     def update(self, instance, validated_data):
#         instance = super(LineItemSerializer, self).update(instance, validated_data)
#         instance.service = validated_data.get('service', {}).get('id')
#         instance.save()
#         return instance