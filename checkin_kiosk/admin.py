from django.contrib import admin

# Register your models here.
from checkin_kiosk.models import Doctor, Appointment


class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['user', 'client_id', 'client_secret', 'access_token']

class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment
    def _session_data(self, obj):
        return obj.get_decoded()


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)