from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .geo_service import search as geo_search
from .models import Location, LocationCategory
from .serializers import LocationRawSerializer, LocationSerializer

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
            print "Serializer is valid"
            # first check if the lat / lng have been registered
            PRECISION = 10000 
            location_query = Location.objects.filter( 
                lat = int( serializer.data.get('lat') * PRECISION ), 
                lng = int( serializer.data.get('lng') * PRECISION )
            )
            print "Location Query:"
            print location_query
            
            if location_query:
                # we have the location, so return it
                loc = location_query[0]
            else:            
                # we don't have the location so look it up and add it
                print "Searching for location"
                search_results = geo_search( 
                    serializer.data.get('lat'), 
                    serializer.data.get('lng')
                )
                if search_results is None:
                    # we failed to translate the coordinates
                    return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
                
                # we succesfully translated the coordinates so create an entry
                
                print serializer.data
                
                # get or create the category object
                loc_category, created = LocationCategory.objects.get_or_create(name=search_results['category'])
                print "create the cat"
                
                # create the location object
                loc = Location.objects.create(
                    name=search_results['name'],
                    lat = int( serializer.data.get('lat') * PRECISION ),
                    lng = int( serializer.data.get('lng') * PRECISION )
                )
                print "created the loc"
                
                # make the association
                loc.categories.add( loc_category )
                print "made the association"

            return Response( LocationSerializer(loc).data, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

