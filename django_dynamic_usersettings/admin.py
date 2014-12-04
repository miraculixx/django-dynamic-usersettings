import django
from distutils.version import StrictVersion
from django.contrib import admin
from django_dynamic_usersettings.models import UserSetting


class UserSettingInline(admin.TabularInline):
    model = UserSetting
    extra = 3


class UserAdmin(admin.ModelAdmin):
    inlines = [UserSettingInline, ]

if StrictVersion(django.get_version()) < StrictVersion('1.7.0'):
    from django.contrib.auth import get_user_model
    from django.conf import settings

    if hasattr(settings, 'DDU_INSERT_INLINE_EDITING'):
        insert_inline_editing = settings.DDU_INSERT_INLINE_EDITING
    else:
        insert_inline_editing = True

    if insert_inline_editing:
        admin.site.unregister(get_user_model())
        admin.site.register(get_user_model(), UserAdmin)


class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'field_name', 'label', 'field_type', 'value')

admin.site.register(UserSetting, UserSettingAdmin)
