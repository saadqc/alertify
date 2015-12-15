from django.conf.urls import patterns, url
from Alerts.views import *
from django.contrib.auth.decorators import login_required

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^$', login_required(AlertView.as_view(), login_url='/login/'), name='alert_view'),
    url(r'^add$', login_required(AlertAddView.as_view(), login_url='/login/'), name='alert_create_view'),
    url(r'^edit$', login_required(AlertEditView.as_view(), login_url='/login/'), name='alert_edit_view'),
]