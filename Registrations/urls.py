from django.conf.urls import url
from Registrations.views import *

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^register$', SignUpUserCreateView.as_view(), name='register_createview'),
    url(r'^login/$', LoginView.as_view(),  name='login_view'),
    url(r'^logout$', LogoutView.as_view(),  name='logout_view'),
    url(r'^forgot$', ForgotPasswordView.as_view(),  name='forgotpassword_view'),
    url(r'^$', HomeView.as_view(),  name='home_view'),
]
