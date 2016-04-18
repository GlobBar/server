from django.contrib import admin
from user_messages.models import NewsMessages


class NewsMessagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'created', 'edit_field')
    list_filter = []

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'body',
            ]})
    ]

    # Actions
    def edit_field(self, obj):
        res = '<span style="padding:5px;"><a href="/admin/user_messages/newsmessages/' + str(
            obj.pk) + '/change/"><span class="changelink">Edit</span></a></span>'
        return res

    edit_field.allow_tags = True
    edit_field.short_description = 'ACTIONS'


admin.site.register(NewsMessages, NewsMessagesAdmin)
