from django.db import models
from django.conf import settings


class UserSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="settings",
    )

    def __str__(self):
        return self.user.username

    def __getattr__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                asObject = ArbitrarySetting.objects.get(
                    setting_id = self.id,
                    key=k,
                )
                return asObject.value
            except ArbitrarySetting.DoesNotExist:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            if k.startswith("as_"):
                asObject, created = ArbitrarySetting.objects.get_or_create(
                    setting_id = self.id,
                    key = k,
                )
                asObject.value = v
                asObject.save()
            else:
                object.__setattr__(self, k, v)
        else:
            object.__setattr__(self, k, v)


class ArbitrarySetting(models.Model):
    setting_id = models.IntegerField()
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

    def __str__(self):
        return "'%s': '%s' for setting ID %s" % (
            self.key,
            self.value,
            self.setting_id,
        )
        
