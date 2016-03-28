from django.contrib import admin
from points.models import PointType, PointsCount


class PointTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'points_count', 'points_count_partner')
    # list_filter = ['title']

    fieldsets = [
        (None, {
            'fields': [
                'title',
                'name',
                'description',
                'enable',
                'points_count',
                'points_count_partner'
            ]}),
    ]


# Count of point for each user
class PointsCountAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'updated',
        'enable',
        'points',
        'user'
    )
    list_filter = ['user']

    fieldsets = [
        (None, {
            'fields': [
                'enable',
                'points',
                'user'
            ]}),
    ]

admin.site.register(PointType, PointTypeAdmin)
admin.site.register(PointsCount, PointsCountAdmin)
