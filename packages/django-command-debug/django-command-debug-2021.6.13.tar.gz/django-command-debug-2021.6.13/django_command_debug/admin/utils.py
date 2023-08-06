from django_command_debug.models import Config, Message

def set_verbose_name_plural():
    Config._meta.verbose_name_plural = 'Configs (%s)' % Config.objects.all().count()
    Message._meta.verbose_name_plural = 'Messages (%s)' % Message.objects.all().count()
