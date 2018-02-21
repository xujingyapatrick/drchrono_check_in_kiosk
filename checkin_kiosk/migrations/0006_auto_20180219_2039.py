# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_kiosk', '0005_appointment_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='average_waiting_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='waiting_duration',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='completed_appointments_counter',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='total_waiting_time',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
