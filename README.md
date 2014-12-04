django-usersettings
===================

Generic settings and API for Django

Read/write dynamic user settings as user.settings.something, and with
API support.

works on Django 1.6+


quick start
===========

1. add to INSTALLED_APPS:

INSTALLED_APPS = (
   ...
   'django_dynamic_usersettings',
   ...
)

2. add to urls.py:

from tastypie.api import Api

from django_dynamic_usersettings.api import UserSettingResource

v1_api = Api(api_name='v1')
v1_api.register(UserSettingResource())


urlpatterns = patterns('',
    ...
    (r'^api/', include(v1_api.urls)),
    ...
)


customize
=========

There are two customizations:

1. the name of the user attribute, by default, it is user.settings.*,
can be changed to user.something_else.*

2. insert inline editing support on the django admin site. By default
it is inserted, if a customized user model is used, maybe setting it
to False is needed.

To customize:

On Django 1.7, inherit
django_dynamic_usersettings.apps.UserSettingsConfig and set
'setting_attribute_name' and 'insert_inline_editing'.

On Django 1.6, set DDU_SETTING_ATTRIBUTE_NAME and
DDU_INSERT_INLINE_EDITING in settings.py  


To run test
===========

1. pip install -r requirements_dev.txt
2. tox

This should run the tests on both Django 1.6 and 1.7
