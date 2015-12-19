# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Groups', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrimeAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Alert', max_length=100)),
                ('alert_state', models.CharField(default=b'pending', max_length=20)),
                ('alert_privacy', models.CharField(max_length=20)),
                ('description', models.CharField(default=b'', max_length=500)),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'last updated')),
                ('rating', models.IntegerField(default=0)),
                ('alert_intensity', models.CharField(default=b'bomb blast', max_length=20)),
                ('groups', models.ManyToManyField(related_name='alert_groups_crime', to='Groups.Group')),
            ],
        ),
        migrations.CreateModel(
            name='MapLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('is_exact_location', models.BooleanField(default=True)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Alert', max_length=100)),
                ('alert_state', models.CharField(default=b'pending', max_length=20)),
                ('alert_privacy', models.CharField(max_length=20)),
                ('description', models.CharField(default=b'', max_length=500)),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'last updated')),
                ('rating', models.IntegerField(default=0)),
                ('alert_intensity', models.CharField(default=b'high', max_length=20)),
                ('groups', models.ManyToManyField(related_name='alert_groups_traffic', to='Groups.Group')),
                ('map_location_from', models.ForeignKey(related_name='location_from', default=None, to='Alerts.MapLocation')),
                ('map_location_to', models.ForeignKey(related_name='location_to', default=None, to='Alerts.MapLocation')),
                ('owner', models.ForeignKey(related_name='alert_owner_traffic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Alert', max_length=100)),
                ('alert_state', models.CharField(default=b'pending', max_length=20)),
                ('alert_privacy', models.CharField(max_length=20)),
                ('description', models.CharField(default=b'', max_length=500)),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'last updated')),
                ('rating', models.IntegerField(default=0)),
                ('alert_intensity', models.CharField(default=b'sunny', max_length=20)),
                ('degree', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(related_name='alert_groups_weather', to='Groups.Group')),
                ('map_location', models.ForeignKey(related_name='alerts_maplocation_weather', default=b'', to='Alerts.MapLocation', max_length=80)),
                ('owner', models.ForeignKey(related_name='alert_owner_weather', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='crimealert',
            name='map_location',
            field=models.ForeignKey(related_name='alerts_maplocation_crime', default=None, to='Alerts.MapLocation'),
        ),
        migrations.AddField(
            model_name='crimealert',
            name='owner',
            field=models.ForeignKey(related_name='alert_owner_crime', to=settings.AUTH_USER_MODEL),
        ),
    ]
