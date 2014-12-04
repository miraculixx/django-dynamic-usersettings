# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_usersettings', '0005_auto_20141126_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersetting',
            old_name='key',
            new_name='label',
        ),
    ]
