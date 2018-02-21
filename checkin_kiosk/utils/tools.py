import datetime
from django.utils import timezone


def get_PST_time_now():
    # get current PST time (San Fransisco).
    return timezone.now()-datetime.timedelta(hours=8)

def get_access_token(request):
    # get access token from local doctor table.
    if request.user.doctor and request.user.doctor.token_expires_timestamp and request.user.doctor.token_expires_timestamp > get_PST_time_now():
        return request.user.doctor.access_token
    return None