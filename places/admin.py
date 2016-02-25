from django.contrib import admin
from places.models import Place


# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_filter = ['title']

    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'address',
                'description',
                'enable',
                'latitude',
                'longitude',
                'image',
            ]}),
        # ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]

admin.site.register(Place, PlaceAdmin)
# admin.site.register(Choice)