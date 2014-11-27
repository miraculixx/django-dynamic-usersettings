# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_usersettings', '0007_auto_20141127_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='label',
            field=models.CharField(default=b'', max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
