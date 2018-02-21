import datetime
from sets import Set

from checkin_kiosk.models import Appointment, Doctor
from checkin_kiosk.utils.constants import AppointmentStatus
from checkin_kiosk.utils.drchrono_api import get_appointments_today, get_patient_information_by_id, \
    update_appointment_information, delete_appointment
from checkin_kiosk.utils.tools import get_PST_time_now


def get_appointments_queryset_today():
    # get today appointments from local database
    today_start = datetime.datetime.combine(get_PST_time_now().date(), datetime.time())
    today_end = datetime.datetime.combine(get_PST_time_now().date() + datetime.timedelta(days=1), datetime.time())

    local_appointments = Appointment.objects.filter(is_active=True, scheduled_timestamp__gte=today_start,
                                                    scheduled_timestamp__lte=today_end)
    print local_appointments
    return local_appointments


def sync_appointments_today_from_drchrono(request):
    # do sync regarding appointment id. Used to retrive today appointemnts from drchrono, and sync local database and
    # drchrono appointments on appointment deleting and adding on drchrono. this will not sync attributes, status.
    local_appointments = get_appointments_queryset_today()
    local_ids = Set([])
    if local_appointments.exists():
        for appointment in local_appointments:
            local_ids.add(str(appointment.drchrono_appointment_id))

    drchrono_appointments = get_appointments_today(request)
    if 'error' in drchrono_appointments:
        return drchrono_appointments
    print drchrono_appointments
    drchrono_ids = Set([])
    for appointment in drchrono_appointments:
        drchrono_ids.add(appointment.get('id'))


    if local_appointments.exists():
        for appointment in local_appointments:
            if str(appointment.drchrono_appointment_id) not in drchrono_ids:
                appointment.is_active = False
                appointment.save()

    for appointment in drchrono_appointments:
        if appointment.get('id') not in local_ids:
            drchrono_appointment_id = appointment.get('id')
            patient_id = appointment.get('patient')
            scheduled_timestamp = appointment.get('scheduled_time')
            dashboard_url = "https://%s.drchrono.com/appointments/%s/" % (
                            request.user.doctor.username, drchrono_appointment_id)
            patient = get_patient_information_by_id(request, patient_id)
            if patient is None:
                continue

            appointment_db = Appointment.create(drchrono_appointment_id=drchrono_appointment_id, patient_id=patient_id, patient_first_name=patient.get('first_name'), patient_last_name=patient.get('last_name'), patient_SSN=patient.get('social_security_number'), scheduled_timestamp=scheduled_timestamp, dashboard_url=dashboard_url)
            appointment_db.save()

    return {"success":'sync success'}


def get_appointment_by_checkin_form(cleaned_data):
    # validate checkin form using local database.
    first_name = cleaned_data.get("first_name")
    last_name = cleaned_data.get("last_name")
    ssn = cleaned_data.get("SSN")
    today_start = datetime.datetime.combine(get_PST_time_now().date(), datetime.time())
    today_end = datetime.datetime.combine(get_PST_time_now().date() + datetime.timedelta(days=1), datetime.time())

    appointment = Appointment.objects.filter(patient_first_name=first_name, patient_last_name=last_name,
                                             patient_SSN=ssn, scheduled_timestamp__gte=today_start,
                                             scheduled_timestamp__lte=today_end)

    if not appointment.exists():
        return None
    return appointment.first()

def update_doctor_waiting_time_and_counter(request, cur_duration):
    total_time = request.user.doctor.total_waiting_time+cur_duration
    counter = request.user.doctor.completed_appointments_counter+1
    doctor = Doctor.objects.filter(user=request.user)
    if doctor.exists():
        doctor = doctor.first()
        doctor.total_waiting_time = total_time
        doctor.completed_appointments_counter = counter
        doctor.save()
        return {'success':'update total waiting time and counter successfully!'}
    return {'error':'cannot find doctor for this user, please login!'}


def update_appointment_status(request, appointment_id, status):
    # update status for both local database and drchrono
    if not AppointmentStatus.is_valid_status(status):
        return {'error': 'status not legal!'}
    # 1.update status on drchrono
    r = update_appointment_information(request,appointment_id,{'status':status} )

    # 2. update status locally
    if 'success' in r:

        if status == AppointmentStatus.ARRIVED:
            appointment = Appointment.objects.filter(drchrono_appointment_id=appointment_id)
            if not appointment.exists():
                return {'error': 'appointment with id: %s does not exist!' % appointment_id}
            appointment = appointment.first()
            appointment.arrive_timestamp = get_PST_time_now()
            appointment.current_status = status
            appointment.save()
            return {'success': 'update appointment status to Arrived'}

        if status == AppointmentStatus.IN_SESSION:
            appointment = Appointment.objects.filter(drchrono_appointment_id=appointment_id)
            if not appointment.exists():
                return {'error': 'appointment with id: %s does not exist!' % appointment_id}
            appointment = appointment.first()
            appointment.start_treatment_timestamp = get_PST_time_now()
            appointment.current_status = status
            duration = 0
            if appointment.arrive_timestamp is not None:
                duration = int(
                    (appointment.start_treatment_timestamp - appointment.arrive_timestamp).total_seconds() / 60)
            appointment.waiting_duration = duration
            appointment.save()

            # update doctor total waiting time and counter
            r = update_doctor_waiting_time_and_counter(request, duration)
            if 'success' not in r:
                return r
            return {'success': 'update appointment status to In Session'}

        if status == AppointmentStatus.COMPLETE:
            appointment = Appointment.objects.filter(drchrono_appointment_id=appointment_id)
            if not appointment.exists():
                return {'error': 'appointment with id: %s does not exist!' % appointment_id}
            appointment = appointment.first()
            appointment.finish_treatment_timestamp = get_PST_time_now()
            appointment.current_status = status
            appointment.save()
            return {'success': 'update appointment status to Complete'}
        return {'success': 'update appointment status to %s'%status}
    return r




def delete_appointment_by_id(request, appointment_id):
    # do delete on local database and drchrono.
    # 1.delete status on drchrono.
    r = delete_appointment(request,appointment_id)

    # 2. delete appointment locally
    if 'success' in r:
        appointment = Appointment.objects.filter(drchrono_appointment_id=appointment_id)
        if not appointment.exists():
            return {'error': 'appointment with id: %s does not exist!' % appointment_id}
        appointment = appointment.first()
        appointment.is_active = False
        appointment.save()
        return {'success': 'update appointment status to Complete'}
    return r







