from django.contrib import admin
from points.models import PointType, PointsCount, FeeSize, Transactions
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from user_messages.models import Messages
from notification.notification_manager import NotificationManager
from points.models import PointsCount
from pytz import timezone
from datetime import datetime

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
        'cst_balance',
        'user'
    )
    # list_filter = ['user']

    fieldsets = [
        (None, {
            'fields': [
                'enable',
                'points',
                'user'
            ]}),
    ]
    def cst_balance(self, obj):
        if obj.balance is None:
            obj.balance = 0
        return str(float(obj.balance)/100)+'$'

class FeeSizeAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = (
        'pk',
        'fee'
    )

    fieldsets = [
        (None, {
            'fields': [
                'fee',
            ]}),
    ]

class TransactionsAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(TransactionsAdmin, self).get_queryset(request)

        return qs.filter(is_success=False, is_error=False)

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = (
        'pk',
        'user',
        'finance_email',
        'cst_amount',
        'description',
        'transaction_actions',
    )

    fieldsets = [
        (None, {
            'fields': [
                'amount',
                'finance_email',
                'description',
            ]}),
    ]

    # Actions
    def get_urls(self):
        urls = super(TransactionsAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<transaction_id>.+)/success/$',
                self.admin_site.admin_view(self.process_success),
                name='transaction-success',
            ),
            url(
                r'^(?P<transaction_id>.+)/error/$',
                self.admin_site.admin_view(self.process_error),
                name='transaction-error',
            ),
        ]
        return custom_urls + urls

    def transaction_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Success</a>&nbsp;'
            '<a class="button" href="{}">Error</a>',
            reverse('admin:transaction-success', args=[obj.pk]),
            reverse('admin:transaction-error', args=[obj.pk]),
        )

    transaction_actions.short_description = 'Transaction Actions'
    transaction_actions.allow_tags = True

    def process_success(self, request, transaction_id, *args, **kwargs):
        transaction = self.get_object(request, transaction_id)
        transaction.is_success = True
        transaction.save()

        # Creating Message
        current_user = request.user
        user = transaction.user
        now_utc = datetime.now(timezone('UTC'))
        body = 'GlobBar successfully transferred you '+str(float(transaction.amount)/100)+'$'
        message = Messages(title='Balance update', body=body, user_from=current_user, user_to=user.id, created=now_utc,
                           is_readed=0)
        message.save()

        # Send notifications
        notify_manager = NotificationManager()
        notify_manager.send_transaction_notify(user, body)

        self.message_user(request, "Changed status on Success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def process_error(self, request, transaction_id, *args, **kwargs):

        transaction = self.get_object(request, transaction_id)
        current_user = request.user
        user = transaction.user
        now_utc = datetime.now(timezone('UTC'))
        if request.method != 'POST':
            return render(request, 'admin/points/transactions/transaction_error2.html',
                          context={'ref': request.META.get('HTTP_REFERER', '/')})

        transaction.is_error = True
        transaction.description = request.POST.get('description')
        transaction.save()

        point_count = PointsCount.objects.get(user=user)
        point_count.balance = point_count.balance + transaction.amount
        point_count.save()

        # Creating Message
        body = transaction.description
        message = Messages(title='Balance update', body=body, user_from=current_user, user_to=user.id, created=now_utc,
                           is_readed=0)
        message.save()

        # Send notifications
        notify_manager = NotificationManager()
        notify_manager.send_transaction_notify(user, body)

        self.message_user(request, "Changed status on Error")
        return HttpResponseRedirect(request.POST.get('ref'))

    def cst_amount(self, obj):
        if obj.amount is None:
            obj.amount = 0
        return str(float(obj.amount)/100)+'$'

admin.site.register(PointType, PointTypeAdmin)
admin.site.register(PointsCount, PointsCountAdmin)
admin.site.register(FeeSize, FeeSizeAdmin)
admin.site.register(Transactions, TransactionsAdmin)
