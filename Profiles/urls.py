from django.conf.urls import url
from Profiles.views import *
from django.contrib.auth.decorators import login_required

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^(?P<id>[0-9]+)/$', login_required(ProfileView.as_view(), login_url='/login/'), name='profile_view'),
    url(r'^image$', login_required(ImageChangeView.as_view(), login_url='/login/'), name='profile_image_view'),
    url(r'^update$', login_required(ChangePasswordView.as_view(), login_url='/login/'), name='profile_update_view'),
    url(r'^get', login_required(ProfileGetView.as_view(), login_url='/login/'), name='profile_get_view'),
]
