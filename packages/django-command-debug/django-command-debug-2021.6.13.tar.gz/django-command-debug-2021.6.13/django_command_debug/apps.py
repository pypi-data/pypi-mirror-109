from django.apps import AppConfig
from django.conf import settings
from django.db.utils import ImproperlyConfigured, OperationalError, ProgrammingError

class Config(AppConfig):
    name = 'django_command_debug'
    verbose_name = 'command-debug'

    def ready(self):
        if 'django.contrib.admin' in settings.INSTALLED_APPS:
            from .admin.utils import set_verbose_name_plural

            try:
                set_verbose_name_plural()
            except (ImproperlyConfigured, OperationalError, ProgrammingError):
                pass
