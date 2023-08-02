from django.apps import AppConfig
from django.conf import settings


class LibrearyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.libreary'

    settings.NUMBERS_BOOKS = 5
    settings.LIMIT_CHARS = 200

 