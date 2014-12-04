# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_dynamic_usersettings', '0002_auto_20141125_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arbitrarysetting',
            name='setting_id',
        ),
        migrations.AddField(
            model_name='arbitrarysetting',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
