import json

from tastypie.authorization import DjangoAuthorization
from tastypie.resources import Resource, convert_post_to_patch
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.validation import Validation
from django_usersettings.models import UserSetting
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from libs import SettingGateWay


class ValueRequiredValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Not quite what I had in mind.'}

        errors = {}

        for field_name in bundle.data:
            if not isinstance(bundle.data[field_name], dict):
                continue
            if not "value" in bundle.data[field_name].keys():
                errors[field_name]= "missing 'value'"

        return errors


class UserSettingResource(Resource):
    class Meta:
        resource_name = 'settings'
        authorization= DjangoAuthorization()
        validation = ValueRequiredValidation() 

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
        self.is_valid(bundle)
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])

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

    def is_valid(self, bundle):
        result = super(UserSettingResource, self).is_valid(bundle)
        
        if bundle.errors:
            raise ImmediateHttpResponse(
                response=self.error_response(bundle.request, bundle.errors))

        return result

    def patch_detail(self, request, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        data = json.loads(request.body)
        for field_name in data:
            content = data[field_name]
            if not isinstance(content, dict):
                continue
            if not content.has_key('value') or content['value'] is None:
                # delete the setting
                try:
                    to_be_delete = UserSetting.objects.get(
                        user = user,
                        field_name = field_name,
                        )
                except UserSetting.DoesNotExist:
                    continue
                else:
                    to_be_delete.delete()
            else:
                # update the setting
                obj, created = UserSetting.objects.get_or_create(
                    user = user,
                    field_name = field_name,
                    value = content['value'],
                    )
                obj.field_type = content.get('type', '')
                obj.label = content.get('label', '')
                obj.save()

    def obj_get_list(self, bundle, **kwargs):
        print bundle.request.user, bundle.request.user.is_staff
        errors = {}
        if not bundle.request.user.is_staff:
            errors['__all__'] = 'You are not allowed to access this'
        elif not hasattr(bundle.request, 'GET'):
            errors['__all__'] = 'Getting all is not supported'
        elif len(bundle.request.GET) == 0:
            errors['__all__'] = 'Getting all is not supported'
        elif len(bundle.request.GET) > 1:
            errors['__all__'] = 'query two or more parameters is not supported'
        else:
            info = bundle.request.GET.items()[0]
            matched = UserSetting.objects.filter(
                field_name = info[0],
                value = info[1])
            return [SettingGateWay(x.user) for x in matched]

        raise ImmediateHttpResponse(
            response=self.error_response(bundle.request, bundle.errors))
        
