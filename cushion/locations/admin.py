from django.contrib import admin

from .models import Location, LocationCategory, Coordinates

class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'account')
    list_display_links = ('id',)
admin.site.register(Coordinates, CoordinatesAdmin)


class LocationCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(LocationCategory, LocationCategoryAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng')
    list_display_links = ('name',)
    
admin.site.register(Location, LocationAdmin)
