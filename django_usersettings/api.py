from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from django_usersettings.models import ArbitrarySetting


class ArbitrarySettingResource(ModelResource):
    class Meta:
        queryset = ArbitrarySetting.objects.all()
        resource_name = 'arbitrary_setting'
        authorization= DjangoAuthorization()
