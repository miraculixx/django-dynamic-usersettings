from django.contrib import admin
from django_usersettings.models import ArbitrarySetting


class ArbitrarySettingInline(admin.TabularInline):
    model = ArbitrarySetting
    extra = 3
    

class ArbitrarySettingAdmin(admin.ModelAdmin):
    list_display=('user', 'key', 'value')
    
admin.site.register(ArbitrarySetting, ArbitrarySettingAdmin)
