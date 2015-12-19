from django.conf.urls import patterns, url
from Alerts.views import *
from django.contrib.auth.decorators import login_required

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^$', login_required(AlertView.as_view(), login_url='/login/'), name='alert_view'),
    url(r'^crime$', login_required(CrimeAlertView.as_view(), login_url='/login/'), name='alert_crime_view'),
    url(r'^weather$', login_required(WeatherAlertView.as_view(), login_url='/login/'), name='alert_weather_view'),
    url(r'^traffic$', login_required(TrafficAlertView.as_view(), login_url='/login/'), name='alert_traffic_view'),
    url(r'^add$', login_required(AlertAddView.as_view(), login_url='/login/'), name='alert_create_view'),
    url(r'^accept$', login_required(AlertAcceptView.as_view(), login_url='/login/'), name='alert_accept_view'),
    url(r'^reject$', login_required(AlertRejectView.as_view(), login_url='/login/'), name='alert_reject_view'),
    url(r'^rate$', login_required(AlertRateView.as_view(), login_url='/login/'), name='alert_rate_view'),
    url(r'^delete$', login_required(AlertDeleteView.as_view(), login_url='/login/'), name='alert_delete_view'),
    url(r'^test', test_url, name='alert_test_view')
]
