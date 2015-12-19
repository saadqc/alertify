import json
import urllib2
from AlertManagement.settings import API_KEY
from BeautifulSoup import BeautifulSoup
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context_processors import csrf
from AlertManagement.Common.utils import update_response, update_response_logged_in, check_moderator
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, View
from Alerts.models import MapLocation, TrafficAlert, WeatherAlert, CrimeAlert
from Groups.models import Group
from django.http.response import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from Registrations.models import User
from django import http
from django.db.models.query_utils import Q
from notifications import notify

__author__ = 'Hp'


class AlertView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.moderator == 'traffic':
            return HttpResponseRedirect(reverse('Alerts:alert_traffic_view'))
        elif request.user.moderator == 'crime':
            return HttpResponseRedirect(reverse('Alerts:alert_crime_view'))
        elif request.user.moderator == 'weather':
            return HttpResponseRedirect(reverse('Alerts:alert_weather_view'))
        else:
            raise Http404


class TrafficAlertView(TemplateView):
    template_name = 'alerts.html'
    model = TrafficAlert
    paginate_by = 30

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(TrafficAlertView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        if self.request.GET.get('state') == 'mine':
            list_alerts = TrafficAlert.objects.filter(owner=self.request.user)
        elif self.request.user.moderator == 'public':
            list_alerts = TrafficAlert.objects.filter(~Q(alert_state='pending'))
        else:
            list_alerts = TrafficAlert.objects.filter(alert_state='pending')
        paginator = Paginator(list_alerts, self.paginate_by)
        if list_alerts.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')

        try:
            alerts = paginator.page(page)
        except PageNotAnInteger:
            alerts = paginator.page(1)
        except EmptyPage:
            alerts = paginator.page(paginator.num_pages)

        context['list_alerts'] = alerts
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context.update(csrf(self.request))
        context.update({'type': 'Traffic'})
        return render_to_response(self.template_name,
                                  context=context)


class CrimeAlertView(TemplateView):
    template_name = 'alerts.html'
    model = CrimeAlert
    paginate_by = 30

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(CrimeAlertView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        if self.request.GET.get('state') == 'mine':
            list_alerts = CrimeAlert.objects.filter(owner=self.request.user)
        elif self.request.user.moderator == 'public':
            list_alerts = CrimeAlert.objects.filter(~Q(alert_state='pending'))
        else:
            list_alerts = CrimeAlert.objects.filter(alert_state='pending')
        paginator = Paginator(list_alerts, self.paginate_by)
        if list_alerts.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')

        try:
            alerts = paginator.page(page)
        except PageNotAnInteger:
            alerts = paginator.page(1)
        except EmptyPage:
            alerts = paginator.page(paginator.num_pages)

        context['list_alerts'] = alerts
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context.update(csrf(self.request))
        context.update({'type': 'Crime'})
        return render_to_response(self.template_name,
                                  context=context)


class WeatherAlertView(TemplateView):
    template_name = 'alerts.html'
    model = WeatherAlert
    paginate_by = 30

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(WeatherAlertView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        if self.request.GET.get('state') == 'mine':
            list_alerts = WeatherAlert.objects.filter(owner=self.request.user)
        elif self.request.user.moderator == 'public':
            list_alerts = WeatherAlert.objects.filter(~Q(alert_state='pending'))
        else:
            list_alerts = WeatherAlert.objects.filter(alert_state='pending')
        paginator = Paginator(list_alerts, self.paginate_by)
        if list_alerts.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')

        try:
            alerts = paginator.page(page)
        except PageNotAnInteger:
            alerts = paginator.page(1)
        except EmptyPage:
            alerts = paginator.page(paginator.num_pages)

        context['list_alerts'] = alerts
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context.update(csrf(self.request))
        context.update({'type': 'Weather'})
        return render_to_response(self.template_name,
                                  context=context)


class AlertAddView(FormView):
    template_name = 'add_alerts.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(AlertAddView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        check_moderator(self.request)
        groups = Group.objects.filter(owner=request.user)
        context = self.get_context_data()
        context.update({'groups': groups})
        context.update(csrf(self.request))
        return render_to_response(template_name=self.template_name,
                                  context=context)

    def post(self, request, *args, **kwargs):
        try:
            check_moderator(self.request)
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            owner_id = request.POST['owner_id']
            alert_type = request.POST.get('alert_type')
            privacy = request.POST.get('privacy')
            intensity = request.POST.get('args[intensity]')
            alert = None

            moderator = User.objects.filter(moderator=alert_type)

            if len(moderator) == 0:
                return JsonResponse({'result': 'moderator not found'})

            user = User.objects.get(id=int(owner_id))
            if alert_type == 'traffic':
                src = (request.POST.get('args[src]')).split(',')
                dest = (request.POST.get('args[dest]')).split(',')
                src_location = MapLocation.objects.create(longitude=float(src[0]),
                                                          latitude=float(src[1]))

                dest_location = MapLocation.objects.create(longitude=float(dest[0]),
                                                           latitude=float(dest[1]))
                alert = TrafficAlert.objects.create(title=title,
                                                      description=desc,
                                                      owner=user,
                                                      alert_privacy=privacy,
                                                      map_location_from=src_location,
                                                      map_location_to=dest_location,
                                                      alert_intensity=intensity
                                                      )
                notify.send(user, recipient=moderator[0],
                            verb='has submitted a traffic alert.',
                            description='Please review the alert.',
                            action_object=alert
                            )

            elif alert_type == 'crime':
                location = (request.POST.get('args[search]')).split(',')
                location = MapLocation.objects.create(longitude=float(location[0]),
                                                      latitude=float(location[1]))
                alert = CrimeAlert.objects.create(title=title,
                                                  description=desc,
                                                  owner=user,
                                                  alert_privacy=privacy,
                                                  map_location=location,
                                                  alert_intensity=intensity
                                                  )

                notify.send(user, recipient=moderator[0],
                            verb='has submitted a crime alert.',
                            description='Please review the alert.',
                            action_object=alert
                            )
            elif alert_type == 'weather':
                location = (request.POST.get('args[search]')).split(',')
                location = MapLocation.objects.create(longitude=float(location[0]),
                                                      latitude=float(location[1]))
                alert = WeatherAlert.objects.create(title=title,
                                                    description=desc,
                                                    owner=user,
                                                    alert_privacy=privacy,
                                                    map_location=location,
                                                    alert_intensity=intensity
                                                    )
                notify.send(user, recipient=moderator[0],
                            verb='has submitted a weather alert.',
                            description='Please review the alert.',
                            action_object=alert,
                            data=dict(actions={})
                            )
            if privacy != 'public':
                group = get_object_or_404(Group, pk=int(privacy))
                if group.owner == request.owner and alert is not None:
                    alert.groups.add(group)
                    alert.save()

            return JsonResponse({'result': 'SUCCESS',
                                 'type': alert_type})
        except Exception as e:
            print e.message
            return JsonResponse({'result': 'ERROR'})


class HttpResponseServerError(HttpResponse):
    status_code = 500


class AlertAcceptView(TemplateView):

    def get_context_data(self, **kwargs):
        if self.request.user.moderator == 'public':
            raise Http404
        """Use this to add extra context."""
        context = super(AlertAcceptView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('alert_id')
            alert_type = request.GET.get('alert_type')
            alert_type = alert_type.lower()
            if alert_type == 'traffic':
                traffic_alert = get_object_or_404(TrafficAlert, pk=int(id))
                traffic_alert.alert_state = 'accept'
                traffic_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_traffic_view'))
            elif alert_type == 'weather':
                weather_alert = get_object_or_404(WeatherAlert, pk=int(id))
                weather_alert.alert_state = 'accept'
                weather_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_weather_view'))
            elif alert_type == 'crime':
                crime_alert = get_object_or_404(CrimeAlert, pk=int(id))
                crime_alert.alert_state = 'accept'
                crime_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_crime_view'))
        except Exception as e:
            print e.message
            return http.HttpResponseServerError('<h1>Server Error (500)</h1>')


class AlertRejectView(TemplateView):
    def get_context_data(self, **kwargs):
        if self.request.user.moderator == 'public':
            raise Http404
        """Use this to add extra context."""
        context = super(AlertRejectView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('alert_id')
            alert_type = request.GET.get('alert_type')
            alert_type = alert_type.lower()
            if alert_type == 'traffic':
                traffic_alert = get_object_or_404(TrafficAlert, pk=int(id))
                traffic_alert.alert_state = 'reject'
                traffic_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_traffic_view'))
            elif alert_type == 'weather':
                weather_alert = get_object_or_404(WeatherAlert, pk=int(id))
                weather_alert.alert_state = 'reject'
                weather_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_weather_view'))
            elif alert_type == 'crime':
                crime_alert = get_object_or_404(CrimeAlert, pk=int(id))
                crime_alert.alert_state = 'reject'
                crime_alert.save()
                return HttpResponseRedirect(reverse('Alerts:alert_crime_view'))
        except Exception as e:
            print e.message
            return http.HttpResponseServerError('<h1>Server Error (500)</h1>')


class AlertRateView(FormView):
    def get_context_data(self, **kwargs):
        if self.request.user.moderator == 'public':
            raise Http404
        """Use this to add extra context."""
        context = super(AlertRateView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def post(self, request, *args, **kwargs):
        try:
            id = request.POST.get('alert_id')
            alert_type = request.POST.get('alert_type')
            alert_rate = request.POST.get('alert_rate')
            alert_type = alert_type.lower()
            if alert_type == 'traffic':
                traffic_alert = get_object_or_404(TrafficAlert, pk=int(id))
                traffic_alert.rating = int(alert_rate)
                traffic_alert.save()
            elif alert_type == 'weather':
                weather_alert = get_object_or_404(WeatherAlert, pk=int(id))
                weather_alert.rating = int(alert_rate)
                weather_alert.save()
            elif alert_type == 'crime':
                crime_alert = get_object_or_404(CrimeAlert, pk=int(id))
                crime_alert.rating = int(alert_rate)
                crime_alert.save()
            return JsonResponse({'result': 'SUCCESS',
                                     'type': alert_type})
        except Exception as e:
            print e.message
            return JsonResponse({'result': 'ERROR'})


class AlertDeleteView(TemplateView):
    def get_context_data(self, **kwargs):
        if self.request.user.moderator == 'public':
            raise Http404
        """Use this to add extra context."""
        context = super(AlertDeleteView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('alert_id')
            alert_type = request.GET.get('alert_type')
            alert_type = alert_type.lower()
            if alert_type == 'traffic':
                traffic_alert = get_object_or_404(TrafficAlert, pk=int(id))
                traffic_alert.delete()
                return HttpResponseRedirect(reverse('Alerts:alert_traffic_view'))
            elif alert_type == 'weather':
                weather_alert = get_object_or_404(WeatherAlert, pk=int(id))
                weather_alert.delete()
                return HttpResponseRedirect(reverse('Alerts:alert_weather_view'))
            elif alert_type == 'crime':
                crime_alert = get_object_or_404(CrimeAlert, pk=int(id))
                crime_alert.delete()
                return HttpResponseRedirect(reverse('Alerts:alert_crime_view'))
        except Exception as e:
            print e.message
            return http.HttpResponseServerError('<h1>Server Error (500)</h1>')


def test_url_weather(request):
    # City = request.user.city
    City = 'Sialkot'
    Country = 'pk'
    url = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s' % (City, Country, API_KEY)
    response = urllib2.urlopen(url)
    html = response.read()
    obj = json.loads(html)
    internet_user = User.objects.get(email='internet@user.com')
    # weather-main, visibility
    weather_state = ''
    for w in obj['weather']:
        weather_state += w['main'] + ', '
    weather_state = weather_state.rstrip(', ')
    weather_map = obj['coord']
    map_location = MapLocation.objects.create(longitude=float(weather_map['lon']),
                                              latitude=float(weather_map['lat']))
    weather = WeatherAlert.objects.create(alert_state='pending',
                                        alert_privacy='public',
                                        owner=internet_user,
                                        map_location=map_location,
                                        alert_intensity=weather_state
                                        )
    return HttpResponse(weather_state)


def test_url(request):
    # City = request.user.city
    City = 'Sialkot'
    Country = 'Pakistan'
    keywords = 'bomb+blast+pakistan'
    url_google = 'http://arynews.tv/en/category/pakistan/'
    response = urllib2.urlopen(url_google)
    html = response.read()
    bs = BeautifulSoup(html)

    news = bs.select('.span-24 .top-news .group-0')

    internet_user = User.objects.get(email='internet@user.com')
    map_location = MapLocation.objects.create(longitude=float(0),
                                              latitude=float(0),
                                              is_exact_location=False,
                                              city=Country)
    crime = CrimeAlert.objects.create(alert_state='pending',
                                        alert_privacy='public',
                                        owner=internet_user,
                                        map_location=map_location,
                                        alert_intensity='Bomb Blast'
                                        )
    return HttpResponse(crime)

