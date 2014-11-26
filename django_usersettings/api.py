from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from django_usersettings.models import UserSetting


class UserSettingResource(ModelResource):
    class Meta:
        queryset = UserSetting.objects.all()
        resource_name = 'arbitrary_setting'
        authorization= DjangoAuthorization()
