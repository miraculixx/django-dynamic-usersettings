# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_usersettings', '0003_auto_20141125_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersetting',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserSetting',
        ),
    ]
