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
            bundle.data[setting.field_name] = {
                'label': setting.label,
                'type': setting.field_type,
                'value': setting.value,
                }
 
        return bundle

    def obj_get(self, bundle, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        return SettingGateWay(user)

    def obj_delete(self, bundle, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        UserSetting.objects.filter(user=user).delete()

    def obj_update(self, bundle, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])

        for field_name in bundle.data:
            if not "value" in bundle.data[field_name].keys():
                return {field_name, "missing 'value'"}
                
        for field_name in bundle.data:
            content = bundle.data[field_name]
            obj, created = UserSetting.objects.get_or_create(
                user = user,
                field_name = field_name,
                value = content['value'],
                )
            obj.field_type = content.get('type', '')
            obj.label = content.get('label', '')
            obj.save()
