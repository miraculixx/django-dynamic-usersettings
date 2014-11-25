from django.db import models
from django.conf import settings


class UserSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="settings",
    )


class ArbitrarySetting(models.Model):
    setting = models.ForeignKey(UserSetting)
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=128)
