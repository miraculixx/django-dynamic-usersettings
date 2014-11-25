from django.db import models
from django.conf import settings


class UserSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="settings",
    )

    def __str__(self):
        return self.user.username


class ArbitrarySetting(models.Model):
    setting = models.ForeignKey(UserSetting)
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

    def __str__(self):
        return "'%s': '%s' for user %s" % (
            self.key,
            self.value,
            self.setting.user.username,
        )
        
