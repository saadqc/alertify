from django.db import models
from optparse import _
from Registrations.models import User

__author__ = 'Hp'


class Group(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='user_owner')
    users = models.ManyToManyField(User, related_name='user_members')
    updated_at = models.DateTimeField(_('last updated'), auto_now_add=True)

    def __unicode__(self):
        return self.name
