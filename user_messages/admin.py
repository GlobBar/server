from django.contrib import admin
from user_messages.models import Messages


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_to', 'title', 'body', 'created')
    list_filter = ['user_to']

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'body',
                'user_to',
                # 'created',
            ]})
    ]

admin.site.register(Messages, MessageAdmin)