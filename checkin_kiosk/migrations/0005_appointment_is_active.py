# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_kiosk', '0004_auto_20180219_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
