from django.conf.urls import url

from checkin_kiosk.views import home_page, login_page, logout_page, register_page, appointment_page, checkin_page, \
    information_page, oauth_page, exit_checkin_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$', logout_page, name='logout'),
    url(r'^register/$', register_page, name='register'),
    url(r'^appointment/$', appointment_page, name='appointment'),
    url(r'^checkin/$', checkin_page, name='checkin'),
    url(r'^exit_checkin/$', exit_checkin_page, name='exit_checkin'),
    url(r'^information/(?P<patient_id>\d+)/', information_page, name='information'),
    url(r'^oauth/$', oauth_page, name='oauth'),

]
