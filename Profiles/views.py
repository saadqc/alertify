import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import JsonResponse
from AlertManagement.settings import BASE_DIR, STATIC_URL
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from AlertManagement.Common.utils import update_response_logged_in
from Alerts.models import TrafficAlert, WeatherAlert, CrimeAlert
from Registrations.models import User
from django.template.context_processors import csrf
from django.views.generic import TemplateView, View, FormView, ListView
from notifications.models import Notification
import os

__author__ = 'Hp'


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=int(kwargs.get('id', -1)))
        traffic_alerts = TrafficAlert.objects.filter(Q(owner=request.user) & ~Q(rating=0))
        weather_alerts = WeatherAlert.objects.filter(Q(owner=request.user) & ~Q(rating=0))
        crime_alerts = CrimeAlert.objects.filter(Q(owner=request.user) & ~Q(rating=0))
        rating = 0
        for alert in traffic_alerts:
            rating += alert.rating
        for alert in weather_alerts:
            rating += alert.rating
        for alert in crime_alerts:
            rating += alert.rating

        total = traffic_alerts.count() + weather_alerts.count() + crime_alerts.count()
        if total == 0:
            total = 1
        result_rating = rating / total

        int_rating = int(result_rating)

        context = self.get_context_data()
        context.update({'profile_user': user,
                        'rating': result_rating,
                        'int_rating': int_rating})
        context.update(csrf(self.request))
        return render_to_response(self.template_name,
                                  context=context
                                  )


class ChangePasswordView(FormView):
    template_name = 'change_password.html'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        new_pass_again = request.POST.get('new_password_again')
        if old_pass != user.password:
            context = self.get_context_data()
            context.update({'profile_user': user, 'error': 'Invalid current password entered'})
            return render_to_response(self.template_name,
                                      context=context)
        elif new_pass != new_pass_again:
            context = self.get_context_data()
            context.update({'profile_user': user, 'error': "Password doesn't match"})
            return render_to_response(self.template_name,
                                      context=context)

        user.set_password(new_pass)
        user.save()

        return HttpResponseRedirect(reverse('Profiles:profile_view', args=(user.id,)))

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        context.update(csrf(self.request))
        context.update({'profile_user': self.request.user})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render_to_response(self.template_name,
                                  context=context)


class ProfileGetView(View):

    def post(self, request, *args, **kwargs):
        search_field = request.POST.get('q')
        ids = request.POST.get('ids')
        ids = ids.split(',')
        if ids is None:
            ids = []
        users = User.objects.filter(Q(first_name__startswith=search_field) | Q(last_name__startswith=search_field))
        list_users = []
        for user in users:
            if str(user.id) not in ids and user.id != request.user.id and user.moderator == 'public':
                list_users.append(dict(label=user.get_full_name(),
                                       value=user.id))
        return JsonResponse(dict(results=list_users))


class ImageChangeView(FormView):

    def post(self, request, *args, **kwargs):
        file_image = request.FILES.get('image')
        file_dir = os.path.join(STATIC_URL, 'media/img/' + str(request.user.id))
        if not os.path.exists(BASE_DIR + "/" + file_dir):
            os.makedirs(BASE_DIR + "/" + file_dir)
        file_path = os.path.join(file_dir, file_image.name)
        if os.path.exists(BASE_DIR + "/" + file_path):
            try:
                os.remove(BASE_DIR + "/" + file_path)
            except Exception:
                print Exception.message
        with open(os.path.join(BASE_DIR + "/" + file_dir, file_image.name), 'wb') as destination:
            for chunk in file_image.chunks():
                destination.write(chunk)
        request.user.profile_img_path = file_path
        request.user.save()
        return HttpResponseRedirect(reverse('Profiles:profile_view', args=(request.user.id,)))


class NotificationView(ListView):
    model = Notification
    template_name = 'notifications/notification.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(NotificationView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        context.update(csrf(self.request))

        list_notifications = self.request.user.notifications.all()
        paginator = Paginator(list_notifications, self.paginate_by)
        if list_notifications.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')

        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        context['list_notifications'] = groups

        return context

