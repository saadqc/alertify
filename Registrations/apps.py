from django.apps import AppConfig

__author__ = 'Saad'


class RegistrationConfig(AppConfig):
    name = 'Registration'
    label = 'fyptask'  # <-- this is the important line - change it to anything other than the default ('Registration' in this case)
