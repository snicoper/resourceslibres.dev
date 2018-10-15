from django.contrib.sitemaps import Sitemap

from .models import Resource


class ResourceSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Resource.objects.published()

    def lastmod(self, obj):
        return obj.create_at
