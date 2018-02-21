# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_name', models.CharField(max_length=255)),
                ('patient_email', models.EmailField(max_length=255)),
                ('patient_phone', models.CharField(max_length=255)),
                ('dashboard_url', models.CharField(default=None, max_length=255, null=True, blank=True)),
                ('current_status', models.CharField(default=b'', max_length=255)),
                ('arrive_timestamp', models.DateTimeField(default=None, null=True, blank=True)),
                ('start_treatment_timestamp', models.DateTimeField(default=None, null=True, blank=True)),
                ('finish_treatment_timestamp', models.DateTimeField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id_drchrono', models.IntegerField()),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('office', models.IntegerField()),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('access_token', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('expires_timestamp', models.DateTimeField()),
                ('average_waiting_time', models.IntegerField()),
            ],
        ),
    ]
