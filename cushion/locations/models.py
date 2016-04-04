from __future__ import unicode_literals

from django.db import models
import logging
LOGGER = logging.getLogger(__name__)


class LocationCategory(models.Model):
    name = models.CharField(max_length=140)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' % ( self.name, )

class Location(models.Model):
    name = models.CharField(max_length=140, blank=True)
    categories = models.ManyToManyField(LocationCategory, related_name='location_categories')
    lat = models.IntegerField()
    lng = models.IntegerField()

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s <%s,%s>' % ( self.name, str(self.lat), str(self.lng) )
