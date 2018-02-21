from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from six import wraps

from drchrono.settings import REDIRECT_URI, AUTH_DRCHRONO_SCOPE


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


def redirect_to_oauth_if_not_oauthed(f):
    # redirect to oauth when request is not oauthed.
    @wraps(f)
    def __decorator(request, *args, **kwargs):
        res = f(request, *args, **kwargs)
        print "res"

        print res.content
        print res
        try:
            data = res.json()
            print 'data'
            print data
            if 'error' in data and 'please do oauth' in data['error']:
                drchrono_oauth_url = "https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s&scope=%s" % (
                    REDIRECT_URI, request.user.doctor.client_id, AUTH_DRCHRONO_SCOPE)
                return HttpResponseRedirect(drchrono_oauth_url)
            return res
        except:
            return res
    return __decorator
