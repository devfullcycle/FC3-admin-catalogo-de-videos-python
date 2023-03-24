from rest_framework import serializers
from core.__seedwork.infra.django_app.serializers import ISO_8601, CollectionSerializer, ResourceSerializer


class CategorySerializer(ResourceSerializer):  # pylint: disable=abstract-method
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)


class CategoryCollectionSerializer(CollectionSerializer):  # pylint: disable=abstract-method
    child = CategorySerializer()
