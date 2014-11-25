from django.apps import AppConfig
from django.contrib.auth import get_user_model
from libs import UserSettingDescriptor


class UserSettingsConfig(AppConfig):
    name = "django_usersettings"
    
    def ready(self):
        setattr(get_user_model(),
                "settings2",
                UserSettingDescriptor(),
            )

        
