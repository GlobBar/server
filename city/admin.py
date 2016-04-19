from django.contrib import admin
from city.models import City


class CityAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    list_per_page = 10

    list_display = ('pk', 'title')
    list_filter = ['title']

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'address',
                # 'enable',
                'time_zone',
                'latitude',
                'longitude',
            ]})
    ]

admin.site.register(City, CityAdmin)
