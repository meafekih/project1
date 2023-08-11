from django.apps import AppConfig
from django.conf import settings

class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crm'

    settings.NUMBERS_BOOKS = 5
    settings.LIMIT_CHARS = 200


    def ready(self):
        import apps.crm.signals.customer