# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_kiosk', '0002_auto_20180218_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='patient_email',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient_name',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient_phone',
        ),
        migrations.AddField(
            model_name='appointment',
            name='drchrono_appointment_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_SSN',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_first_name',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_last_name',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='scheduled_timestamp',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
