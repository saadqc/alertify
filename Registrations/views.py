from django.db.models.query_utils import Q
from AlertManagement import settings
from django import http
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login as django_login, authenticate, \
    logout as django_logout
from django.shortcuts import render, render_to_response, get_object_or_404
from AlertManagement.Common.utils import update_response

# Create your views here.
from django.views.generic import *
from Registrations.EmailMessages import EmailMsg
from Registrations.forms import *
from Registrations.models import User


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class SignUpUserCreateView(AjaxableResponseMixin, CreateView):
    """
    User SignUp form Controller View => get post request from user, validate and store in database
    """
    template_name = "sign_up.html"
    form_class = RegisterUserForm

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(SignUpUserCreateView, self).get_context_data(**kwargs)
        context = update_response(context)
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Registrations:home_view'))
        return HttpResponse('error')


# Login User Form
class LoginView(FormView):
    """
    Login User View => get post requset from user and validate form, login user and then redirect to home view
    """
    template_name = 'sign_in.html'
    form_class = LoginUserForm

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(LoginView, self).get_context_data(**kwargs)
        context = update_response(context)
        return context

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect(reverse('Registrations:home_view'))
            else:
                raise forms.ValidationError("Authentication error.")
        else:
            raise forms.ValidationError("form invalid error.")


# Logout User
class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            django_logout(request)
        return HttpResponseRedirect(reverse('Registrations:home_view'))


# Forgot Password Step 1
class ForgotPasswordView(FormView):
    template_name = 'forgotpassword.html'
    form_class = ForgotPasswordForm1

    def post(self, request, *args, **kwargs):
        form = ForgotPasswordForm1(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            sendEmail = EmailMsg()
            sendEmail.sendForgotPassCode(user)
            return HttpResponseRedirect(reverse('Registrations:login_view'))
        form = ForgotPasswordForm2(request.POST)
        raise forms.ValidationError('Form validation error')


# Home Page View
class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Profiles:profile_view', args=(request.user.id,)))
        else:
            return HttpResponseRedirect(reverse('Registrations:login_view'))


class Success(TemplateView):
    template_name = "sign_in.html"


"""
API - Alert Management
"""


def api_login(request):
    context = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    key = request.POST.get('key')
    if key != settings.API_KEY:
        raise http.HttpResponseForbidden()

    user = get_object_or_404(User, Q(email=email) & Q(password=password))
    context.update({'token': user.bearer_token})
    return context
