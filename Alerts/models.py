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


class Alert(models.Model):
    """
    Show alerts of different types to user
    """
    title = models.CharField(max_length=100, default='Alert')
    owner = models.ForeignKey(User, related_name='alert_owner')
    """
    alert_state => 'pending', 'accepted'
    if 'pending' state then
    """
    alert_state = models.CharField(max_length=20, default='pending')
    # alert_privacy => public, groups
    alert_privacy = models.CharField(max_length=20)
    # if alert_privacy is groups then share alerts with group only
    groups = models.ManyToManyField(Group, related_name='alert_groups')
    # alert type can be "weather","earthquake", "traffic", "bomb blast"
    alert_type = models.CharField(max_length=20)
    description = models.CharField(default='', max_length=500)
    updated_at = models.DateTimeField(_('last updated'), auto_now_add=True)
    map_location = models.ForeignKey(MapLocation, default=None)
    # rating of alert given by moderator. 0 if not rated
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
