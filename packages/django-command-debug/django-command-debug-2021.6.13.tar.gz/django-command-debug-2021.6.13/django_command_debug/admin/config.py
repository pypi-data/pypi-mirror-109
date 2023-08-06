from django.contrib import admin

from django_command_debug.models import Config

from .utils import set_verbose_name_plural

class ConfigAdmin(admin.ModelAdmin):
    list_display = ['id','name','app','is_enabled']
    list_filter = ('app','is_enabled',)
    list_search = ('name',)

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

admin.site.register(Config, ConfigAdmin)
