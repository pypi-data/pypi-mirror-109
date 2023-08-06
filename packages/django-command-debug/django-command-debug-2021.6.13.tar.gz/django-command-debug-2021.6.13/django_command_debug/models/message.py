from django.db import models

class Message(models.Model):
    app = models.TextField(null=True,blank=True,editable=False)
    name = models.TextField(editable=False)
    msg = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)

    class Meta:
        db_table = 'django_command_debug_message'
        indexes = [
           models.Index(fields=['app',]),
           models.Index(fields=['name',]),
           models.Index(fields=['-created_at',]),
        ]
        ordering = ('-created_at',)
