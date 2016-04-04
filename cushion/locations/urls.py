from django.conf.urls import url
from .views import LocationCreateAPIHandler

# API endpoints
urlpatterns = [
    url(r'^locations$',
        LocationCreateAPIHandler.as_view(),
        name='locations-list'),
]
