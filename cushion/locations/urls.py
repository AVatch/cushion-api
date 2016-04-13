from django.conf.urls import url
from .views import LocationCreateAPIHandler, CoordinateLoggerAPIHandler

# API endpoints
urlpatterns = [
    url(r'^locations$',
        LocationCreateAPIHandler.as_view(),
        name='locations-list'),

    url(r'^coordinates$',
        CoordinateLoggerAPIHandler.as_view(),
        name='coordinates-logger'),
]
