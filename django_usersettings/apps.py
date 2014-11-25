from django.apps import AppConfig
from django.contrib.auth import get_user_model
from libs import UserSettingDescriptor


class UserSettingsConfig(AppConfig):
    name = "django_usersettings"
    setting_attribute_name = "settings"
    
    def ready(self):
        setattr(get_user_model(),
                UserSettingsConfig.setting_attribute_name,
                UserSettingDescriptor(),
            )

        
