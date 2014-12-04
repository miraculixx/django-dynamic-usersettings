from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from django_dynamic_usersettings.api import UserSettingResource

v1_api = Api(api_name='v1')
v1_api.register(UserSettingResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
