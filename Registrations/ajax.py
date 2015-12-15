import json
from Registrations.forms import *
from dajaxice.decorators import dajaxice_register

__author__ = 'Saad'


# Register Company Form
@dajaxice_register(method='POST')
def login_user_form(request, form):
    form = LoginUserForm(form)
    if form.is_valid():
        error_msg = "VALID"
    else:
        error_msg = form.errors
    return json.dumps({'message': error_msg})


# Register User Form
@dajaxice_register(method='POST')
def register_user_form(request, form):
    try:
        form = RegisterUserForm(form)
        if form.is_valid():
            error_msg = "VALID"
        else:
            error_msg = form.errors
    except Exception as e:
        print e.message
    return json.dumps({'message': error_msg})


# check forgot password phase 1
@dajaxice_register(method='POST')
def check_forgot_password(request, form):
    form = ForgotPasswordForm1(form)
    if form.is_valid():
        error_msg = "VALID"
    else:
        error_msg = form.errors
    return json.dumps({'message': error_msg})

