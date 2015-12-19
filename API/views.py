import json
from django.utils.timesince import timeuntil
from django.utils import timesince
from Alerts.models import TrafficAlert, WeatherAlert, CrimeAlert, MapLocation
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseServerError
from django.db.models.query_utils import Q
from AlertManagement import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login as django_login, authenticate, \
    logout as django_logout
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from Registrations.models import User
from notifications import notify

"""
API - Alert Management
"""

@csrf_exempt
def api_login(request):
    context = {}
    content = json.loads(request.body)
    email = content['email']
    password = content['password']
    key = content['key']
    if key != settings.API_KEY:
        return HttpResponseForbidden()

    user = authenticate(email=email, password=password)
    if user:
        context.update({'token': user.bearer_token,
                        'name': user.get_full_name(),
                        'user_id': user.id})
        return JsonResponse(context)
    else:
        return HttpResponseServerError()


def check_user(request):
    content = json.loads(request.body)
    token = content['token']
    user_id = content['user_id']
    user = get_object_or_404(User, Q(bearer_token=token) & Q(id=user_id))
    if not user:
        return HttpResponseBadRequest()


@csrf_exempt
def api_get_alerts(request):
    context = {}
    check_user(request)
    traffic_alerts = TrafficAlert.objects.filter(~Q(alert_state='pending'))
    weather_alerts = WeatherAlert.objects.filter(~(Q(alert_state='pending')))
    crime_alerts = CrimeAlert.objects.filter(~(Q(alert_state='pending')))
    alerts = []
    for alert in traffic_alerts:
        alerts.append(alert)

    for alert in weather_alerts:
        alerts.append(alert)

    for alert in crime_alerts:
        alerts.append(alert)

    nAlerts = []
    for alert in alerts:
        new_alert = {'title': alert.title,
                     'description': alert.description,
                     'alert_intensity': alert.alert_intensity,
                     'updated_at': alert.updated_at}
        if isinstance(alert, TrafficAlert):
            new_alert.update({'alert_type': 'Traffic'})
        elif isinstance(alert, WeatherAlert):
            new_alert.update({'alert_type': 'Weather'})
        elif isinstance(alert, CrimeAlert):
            new_alert.update({'alert_type': 'Crime'})

        nAlerts.append(new_alert)
    context.update({'alerts': nAlerts})
    return JsonResponse(context)


@csrf_exempt
def api_create_alert(request):
    check_user(request)
    content = json.loads(request.body)
    title = content['title']
    desc = content['desc']
    owner_id = content['user_id']
    alert_type = content['alert_type']
    intensity = content['intensity']
    privacy = 'public'
    alert = None

    moderator = User.objects.filter(moderator=alert_type)

    if len(moderator) == 0:
        return JsonResponse({'result': 'moderator not found'})

    user = User.objects.get(id=int(owner_id))
    if alert_type == 'traffic':
        src = (content['location']).split(',')
        src_location = MapLocation.objects.create(longitude=float(src[0]),
                                                  latitude=float(src[1]))

        dest_location = MapLocation.objects.create(longitude=float(src[0]),
                                                   latitude=float(src[1]))
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
        location = (content['location']).split(',')
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
        location = (content['location']).split(',')
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
