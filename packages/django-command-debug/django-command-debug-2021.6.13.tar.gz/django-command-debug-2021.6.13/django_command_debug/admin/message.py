from django.contrib import admin
from django.utils.timesince import timesince

from django_command_debug.models import Message

from .utils import set_verbose_name_plural

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','name','app','msg','created_at','created_at_timesince']
    list_filter = ('app','name',)
    list_search = ('msg',)

    def set_verbose_name_plural(self):
        set_verbose_name_plural()

    def delete_model(self, request, obj):
        obj.delete(using=self.using)
        self.set_verbose_name_plural()

    def delete_queryset(self, request, queryset):
        queryset.delete()
        self.set_verbose_name_plural()

    def get_queryset(self, request):
        self.set_verbose_name_plural()
        return super().get_queryset(request)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def created_at_timesince(self, debug):
        return timesince(debug.created_at).split(',')[0]+' ago' if debug.created_at else None
    created_at_timesince.short_description = ''

admin.site.register(Message, MessageAdmin)
