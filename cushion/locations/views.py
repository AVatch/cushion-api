from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .geo_service import search as geo_search
from .models import Location, Coordinates
from .serializers import LocationRawSerializer, LocationSerializer, CoordinatesSerializer


class CoordinateLoggerAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        """
        Log the coordinates and associate them wtih a user
        """
        
        serializer = CoordinatesSerializer( data=request.data )
        
        if serializer.is_valid():
            coords = Coordinates.objects.create(
                latitude = serializer.data.get('latitude'),
                longitude = serializer.data.get('longitude'),
                account = request.user
            )
            return Response( { 'id': coords.id }, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

class LocationCreateAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        """
        Given lat/lng lookup location and store it to the server
        """
        serializer = LocationRawSerializer( data=request.data )
                
        if serializer.is_valid():
            loc = Location.objects.register_location( **serializer.data )
            if loc: 
                return Response( LocationSerializer(loc).data, status=status.HTTP_201_CREATED )
            else:
                return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

