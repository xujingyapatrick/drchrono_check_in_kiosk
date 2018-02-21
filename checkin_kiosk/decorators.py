from django.shortcuts import redirect
from six import wraps


def doctor_mode_required(f):
    # make sure the user in in doctor mode in session before run f.
    @wraps(f)
    def __decorator(request, *args, **kwargs):
        print 'session is_doctor_mode'
        print request.session['is_doctor_mode']

        if not request.session['is_doctor_mode']:
            return redirect('kiosk:exit_checkin')
        return f(request, *args, **kwargs)
    return __decorator
