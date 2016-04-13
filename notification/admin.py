from django.contrib import admin
from notification.models import PushNotifications

class PushNotificationsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    list_display = ('title', 'description', 'count')
    # list_filter = ['title']

    fieldsets = [
        (None, {
            'fields': [
                'title',
                'description',
                'count',
            ]}),
    ]

admin.site.register(PushNotifications, PushNotificationsAdmin)