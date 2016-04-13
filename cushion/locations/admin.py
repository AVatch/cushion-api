from django.contrib import admin

from .models import Location, LocationCategory

class LocationCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(LocationCategory, LocationCategoryAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng')
    list_display_links = ('name',)
    
admin.site.register(Location, LocationAdmin)
