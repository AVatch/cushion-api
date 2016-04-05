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
            # first check if the lat / lng have been registered
            PRECISION = 10000 
            location_query = Location.objects.filter( 
                lat = int( serializer.data.get('lat') * PRECISION ), 
                lng = int( serializer.data.get('lng') * PRECISION )
            )

            if location_query:
                # we have the location, so return it
                loc = location_query[0]
            else:            
                # we don't have the location so look it up and add it
                search_results = geo_search( 
                    serializer.data.get('lat'), 
                    serializer.data.get('lng')
                )
                if search_results is None:
                    # we failed to translate the coordinates
                    return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
                # we succesfully translated the coordinates            
                # look up by name to see if we have the venue
                loc_query = Location.objects.filter( name=search_results['name'] )
                if loc_query:
                    THRESHOLD = 10
                    loc_candidate = loc_query[0]
                    
                    # subtract lat and lng and check if the difference is less than 10 (or some threshold)
                    if ( abs( abs(loc_candidate.lat) - abs( int( serializer.data.get('lat') * PRECISION ) ) ) < THRESHOLD and 
                         abs( abs(loc_candidate.lng) - abs( int( serializer.data.get('lng') * PRECISION ) ) ) < THRESHOLD ):  
                        # if it is, then return that location
                        loc = loc_candidate
                    else:
                        #if it is not, then create that location
                        # get or create the category object
                        loc_category, created = LocationCategory.objects.get_or_create(name=search_results['category'])
                        # create the location object
                        loc = Location.objects.create(
                            name=search_results['name'],
                            lat = int( serializer.data.get('lat') * PRECISION ),
                            lng = int( serializer.data.get('lng') * PRECISION )
                        )
                        
                        # make the association
                        loc.categories.add( loc_category )    
                else:
                    #if it is not, then create that location
                    # get or create the category object
                    loc_category, created = LocationCategory.objects.get_or_create(name=search_results['category'])
                    # create the location object
                    loc = Location.objects.create(
                        name=search_results['name'],
                        lat = int( serializer.data.get('lat') * PRECISION ),
                        lng = int( serializer.data.get('lng') * PRECISION )
                    )
                    
                    # make the association
                    loc.categories.add( loc_category )

            return Response( LocationSerializer(loc).data, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

