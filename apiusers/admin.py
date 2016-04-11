from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from files.models import ProfileImage
from django.conf.urls import url
from django.http import HttpResponseRedirect


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)

    def has_add_permission(self, request):
        return False

    list_display = ['pk', 'cst_user_image', 'username', 'cst_active', 'edit_field']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def cst_user_image(self, obj):
        img_url = ProfileImage.objects.get(owner=obj).image
        res = '<img height="30" width="30" src="%s" />' % (img_url)
        return res

    cst_user_image.allow_tags = True
    cst_user_image.short_description = 'PICTURE'

    # Actions
    def edit_field(self, obj):
        res = '<span style="padding:5px;"><a href="/admin/auth/user/%s/change/"><span class="changelink">Edit</span></a></span>' \
              '<span style="padding:5px;"><a href="/admin/auth/user/%s/delete/"><img src="/static/admin/img/icon-no.svg" alt="False" style="padding: 0 2px 5px 0 ;">' \
              '<span class="Deletelink">Delete</span></a></span>' % (obj.pk, obj.pk)
        return res
    edit_field.allow_tags = True
    edit_field.short_description = 'ACTIONS'

    # IS Active
    def cst_active(self, obj):
        if obj.is_active is True:
            res = '<a href="/admin/auth/user/%s/enable_user/"><img src="/static/admin/img/icon-yes.svg" title="click to disable"></a>' % (obj.pk)
        else:
            res = '<a href="/admin/auth/user/%s/enable_user/"><img src="/static/admin/img/icon-no.svg" title="click to enable" ></a>' % (obj.pk)
        return res
    cst_active.allow_tags = True
    cst_active.short_description = 'IS ACTIVE'

    # Is active handler
    # review_template = 'admin/auth/user/place_view.html'

    def get_urls(self):
        base_urls = super(CustomUserAdmin, self).get_urls()
        view_urlpatterns = [url(r'(.+)/enable_user/$', self.admin_site.admin_view(self.enable_user)), ]
        res_url = view_urlpatterns + base_urls

        return res_url

    def enable_user(self, request, id):
        obj = User.objects.get(pk=id)
        if obj.is_active is True:
            obj.is_active = False
        else:
            obj.is_active = True
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
