from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .geo_service import search as geo_search
from .models import Location, LocationCategory
from .serializers import LocationRawSerializer

import logging
LOGGER = logging.getLogger(__name__)


class LocationCreateAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        """
        Given lat/lng lookup location and store it to the server
        """
        serializer = LocationRawSerializer( data=request.data )
        
        if serializer.is_valid():
            search_results = geo_search( serializer.data.get('lat'), serializer.data.get('lng') )
            if search_results is None:
                # we failed to translate the coordinates
                return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
            
            # we succesfully translated the coordinates so let's check if we already have this location
            location_query = Location.objects.filter( name=search_results.get('name') )
            
            print Location.objects.filter(field__range=(LR, HR))
            
            # loc = Location.objects.get_or_create()
            
            # if location_query:
            #     # we have the location already so let's reference it
            #     loc = location_query[0]
            # else:
            #     # we do not have the location so let's create it
            #     loc = Location.objects.create( lat=serializer.data.get('lat'), 
            #                                    lng=serializer.data.get('lng'),
            #                                    name=geoInfo.get('name') )
            
            # return Response( { 'id': loc.id }, status=status.HTTP_201_CREATED )
            return Response( { }, status=status.HTTP_200_OK )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

