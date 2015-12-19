# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=30, verbose_name=b'first_name')),
                ('last_name', models.CharField(max_length=30, verbose_name=b'last_name')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name=b'email_address')),
                ('gender', models.CharField(default=b'Male', max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'last_updated')),
                ('moderator', models.CharField(default=b'public', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('profile_img_path', models.CharField(default=b'/static/img/default_profile_image.jpg', max_length=512, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'users',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
