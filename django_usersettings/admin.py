from django.contrib import admin
from django_usersettings.models import UserSetting


class UserSettingInline(admin.TabularInline):
    model = UserSetting
    extra = 3
    

class UserAdmin(admin.ModelAdmin):
    inlines = [UserSettingInline,]


class UserSettingAdmin(admin.ModelAdmin):
    list_display=('user', 'field_name', 'value')
    
admin.site.register(UserSetting, UserSettingAdmin)
