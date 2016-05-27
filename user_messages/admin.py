from django.contrib import admin
from user_messages.models import NewsMessages, EmailMessage


class NewsMessagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'created', 'edit_field')
    list_filter = []

    list_per_page = 10

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


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'text_trim', 'created', 'user_to_email',  'edit_field')
    list_filter = []
    raw_id_fields = ("user_to",)

    list_per_page = 10

    fieldsets = [
        (None,               {
            'fields': [
                'subject',
                'text',
                'user_to',
            ]})
    ]

    # Text
    def text_trim(self, obj):
        res = obj.text[0:50]+' ...'
        return res

    text_trim.allow_tags = True
    text_trim.short_description = 'TEXT'

    # Type
    def user_to_email(self, obj):

        if  obj.user_to  is None:
            res = 'To all users'
        else:
            res = 'To <b>'+obj.user_to.email+'</b>'
        return res
    user_to_email.allow_tags = True
    user_to_email.short_description = 'TYPE'

    # Actions
    def edit_field(self, obj):
        res = '<span style="padding:5px;"><a href="/admin/user_messages/emailmessage/' + str(
            obj.pk) + '/change/"><span class="changelink">Edit</span></a></span>'
        return res

    edit_field.allow_tags = True
    edit_field.short_description = 'ACTIONS'


admin.site.register(NewsMessages, NewsMessagesAdmin)
admin.site.register(EmailMessage, EmailMessageAdmin)
