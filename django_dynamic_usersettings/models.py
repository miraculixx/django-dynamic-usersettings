from distutils.version import StrictVersion
import json

import django
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserSetting(models.Model):
    TYPE_STRING = "string"
    TYPE_NUMBER = "number"
    TYPE_BOOL = "bool"
    TYPE_JSON = "json"

    TYPE_CHOICES = (
        (TYPE_STRING, _("string")),
        (TYPE_NUMBER, _("number")),
        (TYPE_BOOL, _("bool")),
        (TYPE_JSON, _("json")),
        )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    field_name = models.CharField(max_length=32)
    label = models.CharField(max_length=128, blank=True, default='')
    field_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_STRING,
        )
    value = models.CharField(max_length=getattr(settings,
                                                'USERSETTING_VALUE_MAXLEN',
                                                4096))

    def __str__(self):
        return "'%s': '%s' for user %s" % (
            self.field_name,
            self.value,
            self.user,
        )
        
    def __unicode__(self):
        return u"'%s': '%s' for user %s" % (
            self.field_name,
            self.value,
            self.user,
        )


class SettingGateWay(object):
    def __init__(self, user):
        self._user = user

    def __getattr__(self, k):
        if k.startswith('_'):
            value = object.__getattribute__(self, k, None)
        else:
            try:
                asObject = UserSetting.objects.get(
                    user=self._user,
                    field_name=k,
                )
            except UserSetting.DoesNotExist:
                value = None
            else:
                try:
                    value = json.loads(asObject.value)
                except:
                    pass
        return value

    def __setattr__(self, k, v):
        if not k.startswith("_"):
            try:
                asObject, created = UserSetting.objects.get_or_create(
                    user=self._user,
                    field_name=k,
                )
                if isinstance(v, (list, tuple, dict)):
                    asObject.type = UserSetting.TYPE_JSON
                elif isinstance(v, int):
                    asObject.type = UserSetting.TYPE_NUMBER
                elif isinstance(v, bool):
                    asObject.type = UserSetting.TYPE_BOOL
                else: 
                    asObject.type = UserSetting.TYPE_STRING
                asObject.value = json.dumps(v)
                if created:
                    asObject.label = k
                asObject.save()
            except:
                raise
        else:
            object.__setattr__(self, k, v)
            
    def __str__(self):
        return "%s" % list(UserSetting.objects.filter(user=self._user))
    
    def __unicode__(self):
        return u"%s" % list(UserSetting.objects.filter(user=self._user))
        

class UserSettingDescriptor(object):
    def __get__(self, instance, owner):
        return SettingGateWay(instance)


if StrictVersion(django.get_version()) < StrictVersion('1.7.0'):
    from django.contrib.auth import get_user_model
    if hasattr(settings, 'DDU_SETTING_ATTRIBUTE_NAME'):
        setting_attribute_name = settings.DDU_SETTING_ATTRIBUTE_NAME
    else:
        setting_attribute_name = "settings"

    setattr(
        get_user_model(),
        setting_attribute_name,
        UserSettingDescriptor(),
    )
