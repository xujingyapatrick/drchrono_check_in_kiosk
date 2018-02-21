from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'', include('checkin_kiosk.urls', namespace='kiosk')),
]
