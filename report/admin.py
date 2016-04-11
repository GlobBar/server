from django.contrib import admin
from report.models import Report
import os
from django.conf import settings
from django.template import RequestContext
from django.conf.urls import url
from django.shortcuts import render_to_response


class Media(Report):
    class Meta:
        proxy = True
        verbose_name = "Image/Video"
        verbose_name_plural = "Added Images/Videos"


# VIDEO/IMAGE
class MediaAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super(MediaAdmin, self).get_queryset(request)
        return qs.filter(type__in=[1, 2])

    list_display = ('pk', 'cst_type', 'cst_thumbnail', 'description', 'venues_name', 'action_field')
    list_filter = ['description', 'place']
    list_display_links = None

    # type
    def cst_type(self, obj):
        type_name = ''
        if obj.type == 1:
            type_name = '<span style="color:#7e5d87;">Image</span>'
        elif obj.type == 2:
            type_name = '<span style="color:#6daaba;">Video</span>'

        return type_name
    cst_type.allow_tags = True
    cst_type.short_description = 'TYPE'

    # thumb
    def cst_thumbnail(self, obj):
        thumb_url = ''

        if obj.report_image is not None:
            # import ipdb;ipdb.set_trace()

            if obj.type == 1:
                # IMAGE
                if obj.report_image.image_thumbnail is not None \
                        and self.is_media_file_exist(str(obj.report_image.image_thumbnail)) is True:
                    thumb_url = str(obj.report_image.image_thumbnail)
            elif obj.type == 2:
                # VIDEO
                if obj.report_image.thumbnail is not None:
                    thumb_url = str(obj.report_image.thumbnail)

        return '<a href="/admin/report/media/%s/review/"><img height="50" src="/media/%s" /></a>' % (obj.pk, thumb_url)

    cst_thumbnail.allow_tags = True
    cst_thumbnail.short_description = 'PICTURE'

    # venues name
    def venues_name(self, obj):
        return obj.place.title

    venues_name.allow_tags = True
    venues_name.short_description = 'VENUES'


    # actions
    def action_field(self, obj):
        res = '' \
              '<span style="padding:5px;"><a href="/admin/report/media/%s/delete/"><img src="/static/admin/img/icon-no.svg" alt="False" style="padding: 0 2px 5px 0 ;">' \
              '<span class="Deletelink">Delete</span></a></span>' % (obj.pk)
        return res
    action_field.allow_tags = True
    action_field.short_description = 'ACTIONS'


    def is_media_file_exist(self, path):
        myfile = settings.MEDIA_ROOT
        myfile += '/'
        myfile += str(path)
        if os.path.isfile(myfile):
            return True

        return False

    # DETAILS TEMPLATE
    review_template = 'admin/report/report/media_view.html'

    def get_urls(self):
        base_urls = super(MediaAdmin, self).get_urls()
        view_urlpatterns = [url(r'(.+)/review/$', self.admin_site.admin_view(self.review)), ]
        res_url  = view_urlpatterns + base_urls

        return res_url

    def review(self, request, id):
        obj = Media.objects.get(pk=id)

        return render_to_response(self.review_template, {
            'title': 'Images/Videos Details',
            'obj': obj,
            # 'thumb_url': thumb_url,
        }, context_instance=RequestContext(request))


class ReportAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super(ReportAdmin, self).get_queryset(request)
        return qs.filter(type__in=[0])

    list_display = ('pk', 'cst_description', 'place', 'created', 'user', 'action_field')
    list_filter = ['place', 'created']
    list_display_links = None



    def cst_description(self, obj):

        report_description = str(obj.description)[0:15]
        res = '<a href="/admin/report/report/%s/review/"><span>%s ...</span>' % (obj.pk, report_description)
        return res
    cst_description.allow_tags = True
    cst_description.short_description = 'REPORT'


    # actions
    def action_field(self, obj):
        res = '' \
              '<span style="padding:5px;"><a href="/admin/report/report/%s/delete/"><img src="/static/admin/img/icon-no.svg" alt="False" style="padding: 0 2px 5px 0 ;">' \
              '<span class="Deletelink">Delete</span></a></span>' % (obj.pk)
        return res
    action_field.allow_tags = True
    action_field.short_description = 'ACTIONS'




    # DETAILS TEMPLATE
    review_template = 'admin/report/report/report_view.html'

    def get_urls(self):
        base_urls = super(ReportAdmin, self).get_urls()
        view_urlpatterns = [url(r'(.+)/review/$', self.admin_site.admin_view(self.review)), ]
        res_url  = view_urlpatterns + base_urls

        return res_url

    def review(self, request, id):
        obj = Report.objects.get(pk=id)

        return render_to_response(self.review_template, {
            'title': 'Report Details',
            'obj': obj,
            # 'thumb_url': thumb_url,
        }, context_instance=RequestContext(request))


admin.site.register(Report, ReportAdmin)
admin.site.register(Media, MediaAdmin)
