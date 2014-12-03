import django
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from distutils.version import StrictVersion

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
        max_length = 16,
        choices = TYPE_CHOICES,
        default = TYPE_STRING,
        )
    value = models.CharField(max_length=128)

    def __str__(self):
        return "'%s': '%s' for user %s" % (
            self.field_name,
            self.value,
            self.user,
        )
        

class SettingGateWay(object):
    def __init__(self, user):
        self._user = user
    
    def __getattr__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                asObject = UserSetting.objects.get(
                    user = self._user,
                    field_name=k,
                )
                return asObject.value
            except UserSetting.DoesNotExist:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            if not k.startswith("_"):
                asObject, created = UserSetting.objects.get_or_create(
                    user = self._user,
                    field_name = k,
                )
                asObject.value = v
                asObject.save()
            else:
                object.__setattr__(self, k, v)
        else:
            object.__setattr__(self, k, v)




class UserSettingDescriptor(object):
    def __get__(self, instance, owner):
        return SettingGateWay(instance)


if StrictVersion(django.get_version()) < StrictVersion('1.7.0'):
    from django.contrib.auth import get_user_model
    if hasattr(settings, 'DDU_SETTING_ATTRIBUTE_NAME'):
        setting_attribute_name = settings.DDU_SETTING_ATTRIBUTE_NAME
    else:
        setting_attribute_name = "settings"
        
    setattr(get_user_model(),
            setting_attribute_name,
            UserSettingDescriptor(),
    )

