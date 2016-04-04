from rest_framework import serializers

from .models import LocationCategory, Location

class LocationRawSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory

class LocationSerializer(serializers.ModelSerializer):
    categories = LocationCategorySerializer(many=True)
    class Meta:
        model = Location