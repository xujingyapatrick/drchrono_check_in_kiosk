from time import sleep
import requests


def doctor_token_watch_dog():
    superuser_login_data = {
        'username':'jxu@itu.edu',
        'password':'9999'
    }
    print "token update start"

    while True:
        with requests.Session() as s:
            # login as superuser
            # get csrf_token first
            r = s.get('http://localhost:8000/admin/login/')
            set_cookie= r.headers['Set-Cookie']
            csrf_token = set_cookie[(set_cookie.index('=')+1):set_cookie.index('; ')]
            superuser_login_data['csrfmiddlewaretoken'] = csrf_token

            # do login
            r = s.post('http://localhost:8000/admin/login/', data=superuser_login_data)
            # update doctor token
            r = s.get('http://localhost:8000/doctor/')

            print "token update finished"
        # run every hour
        sleep(60 * 60)

        # An authorised request.
doctor_token_watch_dog()
