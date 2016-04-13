from rest_framework import serializers

from .models import Coordinates, LocationCategory, Location

class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


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