from django.db import models
from django.conf import settings
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
        

