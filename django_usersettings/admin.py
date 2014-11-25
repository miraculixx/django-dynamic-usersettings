from django.contrib import admin
from django_usersettings.models import UserSetting, ArbitrarySetting


class ArbitrarySettingInline(admin.TabularInline):
    model = ArbitrarySetting
    extra = 3
    

class ArbitrarySettingAdmin(admin.ModelAdmin):
    list_display=('setting', 'key', 'value')
    
admin.site.register(ArbitrarySetting, ArbitrarySettingAdmin)


class UserSettingAdmin(admin.ModelAdmin):
    inlines = [ArbitrarySettingInline,]
    
admin.site.register(UserSetting, UserSettingAdmin)


