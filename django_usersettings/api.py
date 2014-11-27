import json

from tastypie.authorization import DjangoAuthorization
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from django_usersettings.models import UserSetting
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from libs import SettingGateWay


class UserSettingResource(Resource):
    class Meta:
        resource_name = 'settings'
        authorization= DjangoAuthorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj._user.pk
        else:
            kwargs['pk'] = bundle_or_obj._user.pk

        return kwargs
    
    def dehydrate(self, bundle):
        user = bundle.obj._user
        for setting in UserSetting.objects.filter(user=user):
            bundle.data[setting.field_name] = json.dumps({
                'label': setting.label,
                'type': setting.field_type,
                'value': setting.value,
                })
 
        return bundle

    def obj_get(self, bundle, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        return SettingGateWay(user)

    def obj_delete(self, bundle, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        UserSetting.objects.filter(user=user).delete()

