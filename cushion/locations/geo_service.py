import os
import requests
import logging
LOGGER = logging.getLogger(__name__)

GEO_PROVIDER = 'https://api.foursquare.com/v2/venues/search'

# reference: https://developer.foursquare.com/categorytree
GEO_PROVIDER_CATEGORY_EXCLUSION = [
    "530e33ccbcbc57f1066bbfe4",
    "50aa9e094b90af0d42d5de0d",
    "5345731ebcbc57f1066c39b2",
    "530e33ccbcbc57f1066bbff7",
    "4f2a25ac4b909258e854f55f",
    "530e33ccbcbc57f1066bbff8",
    "530e33ccbcbc57f1066bbff3",
    "530e33ccbcbc57f1066bbff9"
]

def process_response(response):
    """
    for now return only the first response in the search array
    as long as it is not a generic neighborhood or something
    """
    for result in response['response']['venues']:
        
        categories = result['categories']    
        primary_category = [ category for category in categories if category['primary'] ][0]
        
        if not set(primary_category['id']).intersection(set(GEO_PROVIDER_CATEGORY_EXCLUSION)):
            LOGGER.info("geo_service.process_response(): Found valid location")
            return {
                'name': result['name'],
                'type': primary_category['pluralName']
            }
    
    LOGGER.error("geo_service.process_response(): Invalid location")
    return None


def search(lat, lng, radius=100):
    """
    perform a query against a geo provider
    """
    params = {
        'll': str(lat) + ',' + str(lng),
        'client_id': os.environ.get("FOURSQUARE_CLIENT_ID"),
        'client_secret': os.environ.get("FOURSQUARE_CLIENT_SECRET"),
        'v': os.environ.get("FOURSQUARE_V")
    }
    response = requests.get(GEO_PROVIDER, params=params)
    
    if response.status_code == 200:
    
        return process_response( response.json() )

    else:
        LOGGER.error("geo_service.search(): " + response)
        return None
    
if __name__=='__main__':
    from os.path import join, dirname
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '../cushion/.env')
    load_dotenv(dotenv_path)
    
    print search(-33.8670,151.1957)
    pass
