from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed

import markdown2

from resources.models import Resource

# Cuando se crea reinstall_dev no hay en la db ninguna
# información y dará un error.
# Se le pone un nombre simbólico hasta que cargue los
# fixtures.
try:
    site_name = Site.objects.get_current().name
except:
    site_name = 'reinstall_dev'


class LastedEntriesFeed(Feed):
    """Feed de últimos recursos."""
    description = 'Recursos gratuitos de programación y diseño, libros y videos'
    title = site_name
    link = '/'

    def items(self, obj):
        return Resource.objects.published().order_by('-id')[:10]

    def item_title(self, obj):
        return obj.title

    def item_description(self, obj):
        return markdown2.markdown(obj.description)

    def item_link(self, obj):
        return obj.get_absolute_url()


class LastedEntriesByCategoryFeed(LastedEntriesFeed):
    """Feeds por categorías."""

    def items(self, obj):
        return obj

    def get_object(self, request, *args, **kwargs):
        return Resource.objects.published().filter(
            categories__slug__exact=kwargs.get('slug')
        ).order_by('-id')


class LastedEntriesByTagFeed(LastedEntriesFeed):
    """Feeds por etiquetas."""

    def items(self, obj):
        return obj

    def get_object(self, request, *args, **kwargs):
        return Resource.objects.published().filter(
            tags__slug__exact=kwargs.get('slug')
        ).order_by('-id')[:10]
