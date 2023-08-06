from django.db import models

class Config(models.Model):
    app = models.TextField(null=True,blank=True)
    name = models.TextField(unique=True)
    is_enabled = models.BooleanField(default=True,verbose_name='enabled')

    class Meta:
        db_table = 'django_command_debug_config'
        indexes = [
           models.Index(fields=['app',]),
           models.Index(fields=['name',]),
        ]
        ordering = ('name',)
