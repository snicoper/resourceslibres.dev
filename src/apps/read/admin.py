from django.contrib import admin

from .models import ReadUserResources


@admin.register(ReadUserResources)
class ResourcesUserReadAdmin(admin.ModelAdmin):
    filter_horizontal = ('resources',)
    list_per_page = 20
    search_fields = ('user',)
    raw_id_fields = ('user',)
