""" Business apps """
from django.apps import AppConfig


class BusinessConfig(AppConfig):
    """ business config """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business'
