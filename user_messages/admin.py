from django.contrib import admin
from user_messages.models import NewsMessages


class NewsMessagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'created')
    list_filter = []

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'body',
                # 'user_to',
                # 'created',
            ]})
    ]

admin.site.register(NewsMessages, NewsMessagesAdmin)
