from django.contrib import admin
from points.models import PointType


# Register your models here.
class PointTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
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


admin.site.register(PointType, PointTypeAdmin)
