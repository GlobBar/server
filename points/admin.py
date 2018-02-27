from django.contrib import admin
from points.models import PointType, PointsCount, FeeSize, Transactions

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

    def make_success(modeladmin, request, queryset):
        queryset.update(is_success=True)

    make_success.short_description = "Success"

    def make_error(modeladmin, request, queryset):
        queryset.update(is_error=True)

    make_error.short_description = "Error"

    list_display = (
        'pk',
        'user',
        'finance_email',
        'cst_amount',
        'description',
    )

    fieldsets = [
        (None, {
            'fields': [
                'amount',
                'finance_email',
                'description',
            ]}),
    ]

    actions = [make_success, make_error]



    def cst_amount(self, obj):

        return str(float(obj.amount)/100)+'$'

admin.site.register(PointType, PointTypeAdmin)
admin.site.register(PointsCount, PointsCountAdmin)
admin.site.register(FeeSize, FeeSizeAdmin)
admin.site.register(Transactions, TransactionsAdmin)
