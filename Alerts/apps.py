from django.apps import AppConfig

__author__ = 'Hp'


class ProfileConfig(AppConfig):
    name = 'Profile'
    label = 'fyptask'  # <-- this is the important line - change it to anything other than the default ('Registration' in this case)
