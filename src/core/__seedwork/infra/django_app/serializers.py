from rest_framework import serializers
from core.__seedwork.application.dto import PaginationOutput

ISO_8601 = '%Y-%m-%dT%H:%M:%S'

class UUIDSerializer(serializers.Serializer): # pylint: disable=abstract-method
    id = serializers.UUIDField()

class PaginationSerializer(serializers.Serializer): # pylint: disable=abstract-method
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()

class ResourceSerializer(serializers.Serializer): # pylint: disable=abstract-method
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'data': data
        }

class CollectionSerializer(serializers.ListSerializer):  # pylint: disable=abstract-method
    pagination: PaginationOutput
    many = False

    def __init__(self, instance: PaginationOutput = None, **kwargs):
        if isinstance(instance, PaginationOutput):
            kwargs['instance'] = instance.items
            self.pagination = instance
        else:
            raise TypeError('instance must be a PaginationOutput')
        super().__init__(**kwargs)

    def to_representation(self, data):
        return {
            'data': [
                # todo - verificar se tem data ou não
                self.child.to_representation(item)['data'] for item in data
            ],
            'meta': PaginationSerializer(self.pagination).data
        }

    @property
    def data(self):
        return self.to_representation(self.instance)