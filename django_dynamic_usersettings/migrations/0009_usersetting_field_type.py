# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dynamic_usersettings', '0008_usersetting_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='field_type',
            field=models.CharField(default=b'string', max_length=16, choices=[(b'string', 'string'), (b'number', 'number'), (b'bool', 'bool'), (b'json', 'json')]),
            preserve_default=True,
        ),
    ]
