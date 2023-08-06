import os
import sys
import traceback


from django.core.management.base import BaseCommand

from django_command_debug.models import Config, Message


class DebugMixin:
    def debug(self,msg):
        app = None
        if 'management.commands.' in type(self).__module__:
            app = type(self).__module__.split('.management.commands')[0].split('.')[-1]
        name = type(self).__module__.split('.')[-1]
        defaults = dict(app=app)
        config, created = Config.objects.get_or_create(defaults,name=name)
        if config.is_enabled:
            Message(name=name,app=app,msg=msg).save()

class DebugCommand(DebugMixin,BaseCommand):
    pass
