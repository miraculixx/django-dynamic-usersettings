from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.contrib import admin

from libs import UserSettingDescriptor
from admin import UserAdmin


class UserSettingsConfig(AppConfig):
    name = "django_dynamic_usersettings"
    setting_attribute_name = "settings"
    insert_inline_editing = True
    
    def ready(self):
        setattr(get_user_model(),
                UserSettingsConfig.setting_attribute_name,
                UserSettingDescriptor(),
            )

        if UserSettingsConfig.insert_inline_editing:
            admin.site.unregister(get_user_model())
            admin.site.register(get_user_model(), UserAdmin)
