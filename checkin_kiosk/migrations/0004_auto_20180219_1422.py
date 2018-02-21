# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_kiosk', '0003_auto_20180219_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='first_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='office',
        ),
    ]
