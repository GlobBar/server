from django.contrib import admin
from points.models import Points


# Register your models here.
class PointsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'enable', 'points_count')
    # list_filter = ['title']

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'description',
                'enable',
                'points_count',
            ]}),
    ]


admin.site.register(Points, PointsAdmin)
