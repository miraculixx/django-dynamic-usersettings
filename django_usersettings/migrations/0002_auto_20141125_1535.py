# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_usersettings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arbitrarysetting',
            name='setting',
        ),
        migrations.AddField(
            model_name='arbitrarysetting',
            name='setting_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
