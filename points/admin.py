from django.contrib import admin
from points.models import PointType, PointsCount

class PointTypeAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_per_page = 10

    list_display = ('pk', 'title', 'points_count', 'points_count_partner')
    # list_filter = ['title']

    fieldsets = [
        (None, {
            'fields': [
                'title',
                # 'name',
                'description',
                'enable',
                'points_count',
                'points_count_partner'
            ]}),
    ]


# Count of point for each user
class PointsCountAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    
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
