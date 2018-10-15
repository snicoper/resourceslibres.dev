from django.contrib import admin

from . import models


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    filter_horizontal = ('resources',)
