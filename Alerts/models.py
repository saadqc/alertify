from django.db import models
from Groups.models import Group
from Registrations.models import User
from optparse import _

__author__ = 'Hp'


class MapLocation(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    # if we don't know exact location then we can turn off exact_location and do not show map
    is_exact_location = models.BooleanField(default=True)
    city = models.CharField(max_length=100)

    def __unicode__(self):
        return self.city


class CrimeAlert(models.Model):
    """
    Show alerts of different types to user
    """
    title = models.CharField(max_length=100, default='Alert')
    owner = models.ForeignKey(User, related_name='alert_owner_crime')
    """
    alert_state => 'pending', 'accepted'
    if 'pending' state then
    """
    alert_state = models.CharField(max_length=20, default='pending')
    # alert_privacy => public, groups
    alert_privacy = models.CharField(max_length=20)
    # if alert_privacy is groups then share alerts with group only
    groups = models.ManyToManyField(Group, related_name='alert_groups_crime')
    # alert type can be "weather", "traffic", "terrorism"
    description = models.CharField(default='', max_length=500)
    updated_at = models.DateTimeField(_('last updated'), auto_now_add=True)
    map_location = models.ForeignKey(MapLocation,related_name='alerts_maplocation_crime', default=None)
    # rating of alert given by moderator. 0 if not rated
    rating = models.IntegerField(default=0)
    # "bomb blast", "robbery", "murder", "voilence"
    alert_intensity = models.CharField(default='bomb blast', max_length=20)

    def __unicode__(self):
        return self.title


class WeatherAlert(models.Model):
    """
        Show alerts of different types to user
        """
    title = models.CharField(max_length=100, default='Alert')
    owner = models.ForeignKey(User, related_name='alert_owner_weather')
    """
    alert_state => 'pending', 'accepted'
    if 'pending' state then
    """
    alert_state = models.CharField(max_length=20, default='pending')
    # alert_privacy => public, groups
    alert_privacy = models.CharField(max_length=20)
    # if alert_privacy is groups then share alerts with group only
    groups = models.ManyToManyField(Group, related_name='alert_groups_weather')
    description = models.CharField(default='', max_length=500)
    updated_at = models.DateTimeField(_('last updated'), auto_now_add=True)
    # city name
    map_location = models.ForeignKey(MapLocation, related_name='alerts_maplocation_weather', default='', max_length=80)
    # rating of alert given by moderator. 0 if not rated
    rating = models.IntegerField(default=0)
    # cloudy, rainy, haze, snowy, hot
    alert_intensity = models.CharField(default='sunny', max_length=20)
    degree = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class TrafficAlert(models.Model):
    """
        Show alerts of different types to user
        """
    title = models.CharField(max_length=100, default='Alert')
    owner = models.ForeignKey(User, related_name='alert_owner_traffic')
    """
    alert_state => 'pending', 'accepted'
    if 'pending' state then
    """
    alert_state = models.CharField(max_length=20, default='pending')
    # alert_privacy => public, groups
    alert_privacy = models.CharField(max_length=20)
    # if alert_privacy is groups then share alerts with group only
    groups = models.ManyToManyField(Group, related_name='alert_groups_traffic')
    description = models.CharField(default='', max_length=500)
    updated_at = models.DateTimeField(_('last updated'), auto_now_add=True)
    # from
    map_location_from = models.ForeignKey(MapLocation, default=None, related_name='location_from')
    # to
    map_location_to = models.ForeignKey(MapLocation, default=None, related_name='location_to')
    # rating of alert given by moderator. 0 if not rated
    rating = models.IntegerField(default=0)
    # blocked, high, medium, low
    alert_intensity = models.CharField(default='high', max_length=20)

    def __unicode__(self):
        return self.title
