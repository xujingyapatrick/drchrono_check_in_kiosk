from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Doctor(models.Model):
    doctor_id_drchrono = models.IntegerField(null=True, blank=True, default=None)
    username = models.CharField(max_length=255, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)

    access_token = models.CharField(max_length=200, null=True, blank=True, default=None)
    refresh_token = models.CharField(max_length=200, null=True, blank=True, default=None)
    token_expires_timestamp = models.DateTimeField(auto_now_add=False, null=True, blank=True, default=None)

    total_waiting_time = models.IntegerField(null=True, blank=True, default=0)
    completed_appointments_counter = models.IntegerField(null=True, blank=True, default=0)

    @classmethod
    def create(cls, user, client_id, client_secret):
        doctor = cls(doctor_id_drchrono=None, username = None, user=user,
                     client_id=client_id, client_secret=client_secret, access_token=None, refresh_token=None,
                     token_expires_timestamp=None, total_waiting_time=0, completed_appointments_counter=0)
        return doctor


class Appointment(models.Model):
    drchrono_appointment_id = models.IntegerField(null=True, blank=True, default=None)
    patient_id = models.IntegerField(null=True, blank=True, default=None)

    patient_first_name = models.CharField(max_length=255,null=True, blank=True, default=None)
    patient_last_name = models.CharField(max_length=255,null=True, blank=True, default=None)
    patient_SSN = models.CharField(max_length=255,null=True, blank=True, default=None)
    scheduled_timestamp = models.DateTimeField(null=True, blank=True, default=None)

    dashboard_url = models.CharField(max_length=255, null=True, blank=True, default=None)
    current_status = models.CharField(max_length=255, default="")
    arrive_timestamp = models.DateTimeField(null=True, blank=True, default=None)
    start_treatment_timestamp = models.DateTimeField(null=True, blank=True, default=None)
    finish_treatment_timestamp = models.DateTimeField(null=True, blank=True, default=None)
    waiting_duration = models.IntegerField(null=True, blank=True, default=None)

    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, drchrono_appointment_id, patient_id, patient_first_name, patient_last_name, patient_SSN, scheduled_timestamp, dashboard_url):
        appointment = cls(drchrono_appointment_id=drchrono_appointment_id, patient_id=patient_id, patient_first_name=patient_first_name, patient_last_name=patient_last_name, patient_SSN=patient_SSN,
                     scheduled_timestamp=scheduled_timestamp, dashboard_url=dashboard_url, current_status="", arrive_timestamp=None,
                     start_treatment_timestamp=None, finish_treatment_timestamp=None)
        return appointment