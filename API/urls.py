from django.conf.urls import url
from API.views import *

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^login/$', api_login, name='register_login'),
    url(r'^alerts/$', api_get_alerts, name='alert_view'),
    url(r'^create/$', api_create_alert, name='alert_create_view'),
]
