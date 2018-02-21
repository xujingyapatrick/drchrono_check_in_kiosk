import datetime
import requests

from checkin_kiosk.models import Doctor
from checkin_kiosk.utils.tools import get_access_token, get_PST_time_now


def get_doctor_information_by_accesstoken(access_token):
    if access_token is None:
        return {'error': 'get access token failed, please do oauth'}
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    data = response.json()
    return data

def refresh_oauth_token(request, doctor=None):
    if doctor is None:
        access_token = get_access_token(request)
        refresh_token = request.user.doctor.refresh_token
        client_id = request.user.doctor.client_id
        client_secret = request.user.doctor.client_secret
        doctor = Doctor.objects.filter(user=request.user)
        if doctor.exists():
            doctor = doctor.first()
        else:
            doctor=None
    else:
        access_token = doctor.access_token
        refresh_token = doctor.refresh_token
        client_id = doctor.client_id
        client_secret = doctor.client_secret

    if access_token is None:
        return {"error":"Current doctor is not oauthed"}

    response = requests.post('https://drchrono.com/o/token/', data={
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    response.raise_for_status()
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = get_PST_time_now() + datetime.timedelta(seconds=data['expires_in'])

    if doctor is not None:
        doctor.access_token = access_token
        doctor.refresh_token = refresh_token
        doctor.token_expires_timestamp = expires_timestamp
        doctor.save()
        return {'success':'refresh token success'}
    return {"error":"Current user is not doctor"}

def get_patient_information_by_id(request, patient_id):
    # should provide patient_id in drchrono
    access_token = get_access_token(request)
    if access_token is None:
        return {'error': 'get access token failed, please do oauth'}
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    patient_url = 'https://drchrono.com/api/patients/%s' % patient_id
    r = requests.get(patient_url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def update_patient_information(request, patient_id, data):
    # update patient demographic info regarding attributes in data
    access_token = get_access_token(request)
    if access_token is None:
        return {'error': 'get access token failed, please do oauth'}
    url = 'https://drchrono.com/api/patients/%s' % patient_id
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    r = requests.patch(url, headers=headers, data=data)
    # r.raise_for_status()
    if r.status_code == 204:
        return {'success': 'update patient information success!',
                'patient_id': patient_id}
    return {'error': 'update patient information failed',
            'patient_id': patient_id,
            'detailed info': r.json()}


def get_appointments_today(request):
    # doctor should be login in, today appointments in drchrono
    access_token = get_access_token(request)
    if access_token is None:
        return {'error': 'get access token failed, please do oauth'}
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    appointments = []
    appointments_url = 'https://drchrono.com/api/appointments'
    while appointments_url:
        r = requests.get(appointments_url, headers=headers, params={'date': get_PST_time_now().date()})
        if r.status_code != 200:
            return {'error': 'get access token failed, please do oauth'}
        data = r.json()
        appointments.extend(data['results'])
        appointments_url = data['next']  # A JSON null on the last page

    return appointments


def update_appointment_information(request, appointment_id, data):
    # update appointment information on drchrono regarding attributes in data.
    access_token = get_access_token(request)
    if access_token is None:
        return {'error': 'get access token failed, please do oauth'}
    url = 'https://drchrono.com/api/appointments/%s' % appointment_id
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    r = requests.patch(url, headers=headers, data=data)
    r.raise_for_status()
    if r.status_code == 204:
        return {'success': 'update patient information success!',
                'appointment_id': appointment_id}
    return {'error': 'update patient information failed',
            'appointment_id': appointment_id,
            'detailed info': r.json()}

def delete_appointment(request, appointment_id):
    # delete appointment in drchrono
    access_token = get_access_token(request)
    headers = {
        # 'Content-Type':'multipart/form-data',
        'Authorization': 'Bearer %s' % access_token,
    }
    url = 'https://drchrono.com/api/appointments/%s'%appointment_id
    r = requests.delete(url, headers=headers)

    if r.status_code == 204:  # HTTP 204 DELETE success
        return {'success': 'appointment delete success!',
                'appointment_id': appointment_id}
    return {'error': 'delete appointment failed',
            'appointment_id': appointment_id}

