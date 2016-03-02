from django.contrib import admin
from city.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_filter = ['title']

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'address',
                'enable',
                'time_zone',
                'latitude',
                'longitude',
            ]})
    ]

admin.site.register(City, CityAdmin)
