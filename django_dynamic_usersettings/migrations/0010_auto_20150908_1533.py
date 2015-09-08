# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_usersettings', '0009_usersetting_field_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='value',
            field=models.CharField(max_length=4096),
        ),
    ]
