from rest_framework import serializers

#Allows Creation/Updating of related model fields with OBJECT instead of just id
class ModelRelatedField(serializers.RelatedField):
    model = None
    pk = 'id'
    serializer = None
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', self.model)
        self.pk = kwargs.pop('pk', self.pk)
        self.serializer = kwargs.pop('serializer', self.serializer)
        assert self.model is not None, (
            'Must set model for ModelRelatedField'
        )
        assert self.serializer is not None, (
            'Must set serializer for ModelRelatedField'
        )
        self.queryset = kwargs.pop('queryset', self.model.objects.all())
        super(ModelRelatedField, self).__init__(**kwargs)
    def to_internal_value(self, data):
        if isinstance(data, int):
            kwargs = {self.pk:data}
            return self.model.objects.get(**kwargs)
        if isinstance(data,dict) and data.get(self.pk,None):
            return self.model.objects.get(id=data['id'])
        if isinstance(data,self.model) and hasattr(data,self.pk):
            return self.model.objects.get(id=getattr(data,self.pk))
        return None
    def to_representation(self, value):
        return self.serializer(value).data
