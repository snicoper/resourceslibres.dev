from django.conf import settings
from django.contrib.sites.models import Site


def common_template_vars(request):
    """Variables comunes en los templates."""
    context = {
        'SITE': Site.objects.get_current(),
        'PROTOCOL': 'https://' if request.is_secure() else 'http://',
        'DISQUS_SHORTNAME': settings.DISQUS_SHORTNAME
    }

    if settings.DEBUG and getattr(settings, 'ADSENSE_IMAGES_FAKE', False):
        context['ADSENSE_IMAGES_FAKE'] = settings.ADSENSE_IMAGES_FAKE
    return context
