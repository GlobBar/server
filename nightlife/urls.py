"""nightlife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from files.views import ConvertTokenViewCustom


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('places.urls')),
    url(r'^', include('notification.urls')),
    url(r'^', include('points.urls')),
    url(r'^', include('report.urls')),
    url(r'^', include('apiusers.urls')),
    url(r'^', include('files.urls')),
    url(r'^', include('friends.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/convert-token/?$', ConvertTokenViewCustom.as_view(), name="convert_token"),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                                }),

]

urlpatterns += staticfiles_urlpatterns()

