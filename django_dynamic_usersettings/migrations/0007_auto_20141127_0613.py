# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_usersettings', '0006_auto_20141127_0354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersetting',
            old_name='label',
            new_name='field_name',
        ),
    ]
