from django.contrib import admin
from places.models import Place
from django.template import RequestContext
from django.conf.urls import url
from django.shortcuts import render_to_response
from places.models import Place
from django import forms


class VenuesAdmin(admin.ModelAdmin):

    list_display = ('pk', 'cst_logo', 'cst_title', 'address', 'is_partner', 'edit_field')
    list_filter = ['title', 'address', 'is_partner']

    list_per_page = 10

    # Logo
    def cst_logo(self, obj):
        return '<img height="30" src="/media/%s" />' % (obj.logo)
    cst_logo.allow_tags = True
    cst_logo.short_description = 'PICTURE'

    # Edit
    def edit_field(self, obj):
        res = '<span style="padding:5px;"><a href="/admin/places/place/%s/change/"><span class="changelink">Edit</span></a></span>' \
              '<span style="padding:5px;"><a href="/admin/places/place/%s/delete/"><img src="/static/admin/img/icon-no.svg" alt="False" style="padding: 0 2px 5px 0 ;">' \
              '<span class="Deletelink">Delete</span></a></span>' % (obj.pk, obj.pk)
        return res
    edit_field.allow_tags = True
    edit_field.short_description = 'ACTIONS'

    # Title
    def cst_title(self, obj):
        return '<a href="/admin/places/place/%s/review/"><span>%s</span></a>' % (obj.pk, obj.title)
    cst_title.allow_tags = True
    cst_title.short_description = 'TITLE'


    fieldsets = [
        (None,               {
            'fields': [
                'title',
                'city',
                'address',
                'description',
                'opening_hours',
                'music_type',
                'age_group',
                'enable',
                'is_partner',
                'latitude',
                'longitude',
                'logo',
                'image',
            ]}),
        # ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]

    review_template = 'admin/places/place/place_view.html'

    def get_urls(self):
        base_urls = super(VenuesAdmin, self).get_urls()
        view_urlpatterns = [url(r'(.+)/review/$', self.admin_site.admin_view(self.review)), ]
        res_url  = view_urlpatterns + base_urls

        return res_url

    def review(self, request, id):
        entry = Place.objects.get(pk=id)

        return render_to_response(self.review_template, {
            'title': 'Venue Details: %s' % entry.title,
            'entry': entry,
        }, context_instance=RequestContext(request))

admin.site.register(Place, VenuesAdmin)
# admin.site.register(Choice)