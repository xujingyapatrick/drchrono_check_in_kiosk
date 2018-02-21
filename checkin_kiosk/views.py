import datetime
import requests
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.views.generic import ListView

from checkin_kiosk.decorators import doctor_mode_required, redirect_to_oauth_if_not_oauthed
from checkin_kiosk.forms import LoginForm, RegisterForm, CheckinForm, InformationForm
from checkin_kiosk.models import Doctor, Appointment
from checkin_kiosk.utils.constants import AppointmentStatus
from checkin_kiosk.utils.drchrono_api import update_patient_information, get_doctor_information_by_accesstoken, \
    refresh_oauth_token
from checkin_kiosk.utils.local_api import get_appointment_by_checkin_form, get_appointments_queryset_today, \
    sync_appointments_today_from_drchrono, get_PST_time_now, update_appointment_status, delete_appointment_by_id
from checkin_kiosk.utils.tools import get_access_token
from drchrono.settings import REDIRECT_URI, AUTH_DRCHRONO_SCOPE


def home_page(request):
    # home
    context = {
               'session': {'is_doctor_mode': request.session.get('is_doctor_mode', False)}
               }
    print context

    return render(request, "home.html", context)


@user_passes_test(lambda u: u.is_superuser)
def doctors_update_tokens(request):

    qs = Doctor.objects.all()
    print qs
    if qs.exists():
        for doctor in qs:
            if doctor.token_expires_timestamp and get_PST_time_now()+datetime.timedelta(hours=6) > doctor.token_expires_timestamp and get_PST_time_now() < doctor.token_expires_timestamp:
                refresh_oauth_token(request=request, doctor=doctor)

    return JsonResponse({'success':'update doctors access token success'},status=200)


def login_page(request):
    # login and set user to doctor mode
    form = LoginForm(request.POST or None)
    context = {
        'form': form,
    }
    print context

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # check if the user is in the database
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

            # do oauth if Oauth is expired
            if not request.user.doctor.token_expires_timestamp or request.user.doctor.token_expires_timestamp < get_PST_time_now():
                drchrono_oauth_url = "https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s&scope=%s" % (
                    REDIRECT_URI, request.user.doctor.client_id, AUTH_DRCHRONO_SCOPE)
                request.session['is_doctor_mode'] = True
                return HttpResponseRedirect(drchrono_oauth_url)

            request.session['is_doctor_mode'] = True
            return redirect("/")
    return render(request, "auth/login.html", context)


def register_page(request):
    # doctor should install app in drchrono account before register
    # create new user, doctor, and  update doctor.
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        client_id = form.cleaned_data.get("client_id").strip()
        client_secret = form.cleaned_data.get("client_secret").strip()
        user = User.objects.create_user(username=username, password=password)

        doctor = Doctor.create(user=user, client_id=client_id, client_secret=client_secret)
        try:
            doctor.save()
            login(request, user)
            request.session['is_doctor_mode'] = True
        except Exception as e:
            return JsonResponse({'error': 'create doctor error',
                                 'exception': str(e)})
        # do oauth by redirecting to drchrono
        drchrono_oauth_url = "https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s&scope=%s" % (
            REDIRECT_URI, client_id, AUTH_DRCHRONO_SCOPE)
        return HttpResponseRedirect(drchrono_oauth_url)

    context = {'page_name': "home",
               'form': form
               }
    print context

    return render(request, "auth/register.html", context)


@login_required
@doctor_mode_required
def oauth_page(request):
    # do oauth in register function and refresh on POST
    if request.method == 'POST':
        r = refresh_oauth_token(request)
        if 'success' in r:
            return redirect('kiosk:oauth')
        return JsonResponse(r)

    # get new token when request.GET has code param
    if request.GET.get('code', None) is None:
        context = {
            'redirect_uri':REDIRECT_URI,
            'client_id':request.user.doctor.client_id,
            'auth_scope':AUTH_DRCHRONO_SCOPE,
            'is_oauthed':False,
            'session': {'is_doctor_mode': request.session.get('is_doctor_mode', False)}
        }
        access_token = get_access_token(request)
        if access_token is not None:
            context['is_oauthed'] = True
        return render(request, 'auth/oauth.html',context)
    else:
        code = request.GET['code']
        # print "code: "+str(code)
        response = requests.post('https://drchrono.com/o/token/', data={
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': request.user.doctor.client_id,
            'client_secret': request.user.doctor.client_secret,
        })
        response.raise_for_status()
        data = response.json()

        doctor = Doctor.objects.filter(user=request.user)
        if not doctor.exists():
            return JsonResponse({'error': 'cannot find doctor of user: %s' % request.user.username})
        doctor = doctor.first()
        doctor.access_token = data['access_token']
        doctor.refresh_token = data['refresh_token']
        doctor.token_expires_timestamp = get_PST_time_now() + datetime.timedelta(seconds=data['expires_in'])
        doctor.save()
        drchrono_doctor_info = get_doctor_information_by_accesstoken(doctor.access_token)
        print drchrono_doctor_info
        doctor.doctor_id_drchrono = drchrono_doctor_info.get('doctor')
        doctor.username = drchrono_doctor_info.get('username')
        doctor.save()
        return redirect('/')


def logout_page(request):
    # logout, go back to login
    auth.logout(request)
    return redirect('/login/')


class AppointmentListView(ListView):

    template_name = "doctor/appointments.html"

    def get_queryset(self):
        # today appointments
        return get_appointments_queryset_today().order_by('scheduled_timestamp')

    def get_context_data(self, *args, **kwargs):
        # add attributes in context for templetes.
        request = self.request
        context = super(AppointmentListView, self).get_context_data(*args, **kwargs)
        total_time = request.user.doctor.total_waiting_time
        count = request.user.doctor.completed_appointments_counter
        context['session'] = {'is_doctor_mode': request.session.get('is_doctor_mode', False)}
        if count == 0:
            context['average_waiting_time'] = 0
        else:
            context['average_waiting_time'] = int(total_time / count)
        return context


@login_required
@doctor_mode_required
def appointment_page(request):
    # appointment page on GET
    if request.method == 'GET':
        return AppointmentListView.as_view()(request)

    # change appointment status according actions in POST
    if request.method == 'POST':
        data = request.POST
        print data
        if request.is_ajax():
            drchrono_appointment_id = data.get('appointment_id')
            appointment = Appointment.objects.filter(drchrono_appointment_id=drchrono_appointment_id)
            if appointment.exists():
                appointment = appointment.first()
                print 'here'
                return JsonResponse({'appointment_status':appointment.current_status}, status=200)
            return JsonResponse({'appointment_status':AppointmentStatus.EMPTY},status=404)

        if data.get('action') == 'start_session':
            r = update_appointment_status(request, data.get('appointment_id'), AppointmentStatus.IN_SESSION)
            if 'success' not in r:
                return JsonResponse(r)
        if data.get('action') == 'finish_session':
            r = update_appointment_status(request, data.get('appointment_id'), AppointmentStatus.COMPLETE)
            if 'success' not in r:
                return JsonResponse(r)
        if data.get('action') == 'cancel_appointment':
            r = delete_appointment_by_id(request, data.get('appointment_id'))
            if 'success' not in r:
                return JsonResponse(r)
        if data.get('action') == 'sync_appointment':
            r = sync_appointments_today_from_drchrono(request)
            if 'success' not in r:
                return JsonResponse(r)

    return redirect('kiosk:appointment')

@login_required
def checkin_page(request):
    # patient checkin.
    request.session['is_doctor_mode'] = False
    form = CheckinForm(request.POST or None)
    context = {
        'form': form,
    }
    print context
    if form.is_valid():
        appointment = get_appointment_by_checkin_form(form.cleaned_data)
        # print reverse('kiosk:information')
        request.session['appointment_id'] = appointment.drchrono_appointment_id

        return redirect('kiosk:information', patient_id=appointment.patient_id)
    return render(request, 'patient/checkin.html', context)

@login_required
def exit_checkin_page(request):
    # Make sure only current doctor can exit checkin mode by asking doctor credentials.
    form = LoginForm(request.POST or None)

    context = {
        'form': form,
    }
    print context

    if form.is_valid():
        username = form.cleaned_data.get('username')
        if username == request.user.username:
            request.session['is_doctor_mode'] = True
            return redirect("/")
    return render(request, "patient/exit_checkin.html", context)

@login_required
def information_page(request, patient_id):
    # update patient demographic information
    request.session['is_doctor_mode'] = False
    print request.method
    form = InformationForm(request.POST or None)
    print form.is_valid()
    if request.method == 'GET':
        context = {'patient_id': patient_id,
                   'form': form,
                   'session': {'is_doctor_mode': request.session.get('is_doctor_mode', False)},
                   }
        return render(request, 'patient/information.html', context)

    if request.method == 'POST':
        data = request.POST
        print data
        if data.get('action', '') == 'skip':
            r = update_appointment_status(request, request.session.get('appointment_id'), AppointmentStatus.ARRIVED)
            if 'success' in r:
                return redirect('kiosk:checkin')
            else:
                return JsonResponse(r)

        elif form.is_valid():
            data = form.cleaned_data
            print data
            patient_info = {}
            for key in data:
                if data.get(key, '') != '' and data.get(key, '') is not None:
                    patient_info[key] = data.get(key, None)
            print patient_info
            r = update_patient_information(request, patient_id, patient_info)
            if 'success' in r:
                r_appointment = update_appointment_status(request, request.session.get('appointment_id'), AppointmentStatus.ARRIVED)
                if 'success' in r_appointment:

                    return redirect('kiosk:checkin')
                else:
                    return JsonResponse(r_appointment)
            else:
                return JsonResponse(r)

    return redirect('kiosk:checkin')
