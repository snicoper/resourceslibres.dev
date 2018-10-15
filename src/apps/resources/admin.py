from django.contrib import admin
from django.utils.html import mark_safe

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(models.ResourceFormat)
class ResourceFormatAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    search_fields = ('title', 'owner__username')
    list_filter = ('active',)
    list_per_page = 20
    list_display = (
        '__str__',
        'owners',
        'active',
        'views',
        'clicks',
        'marked_spam',
        'marked_broken'
    )
    filter_horizontal = (
        'categories',
        'tags',
        'languages'
    )

    def owners(self, obj):
        """Obtener link del owner para list_display."""
        link_to_owner = '/admin/accounts/user/{}/change/'.format(obj.owner.pk)
        url_to_edit = '<a href="{}">{}</a>'.format(link_to_owner, obj.owner.username)
        return mark_safe(url_to_edit)


@admin.register(models.Ratio)
class RatioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'score')


@admin.register(models.QuickResource)
class QuickResourceAdmin(admin.ModelAdmin):
    list_display = ('owner', 'link')
