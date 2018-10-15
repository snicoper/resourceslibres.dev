import os

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from . import models


@receiver(post_delete, sender=models.Category)
def delete_category_handler(sender, instance, **kwargs):
    """Si existe, elimina la imagen del disco."""
    if instance.image and os.path.exists(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=models.Language)
def delete_language_handler(sender, instance, **kwargs):
    """Si existe, elimina la imagen del disco."""
    if instance.image and os.path.exists(instance.flag.path):
        os.remove(instance.flag.path)


@receiver(post_delete, sender=models.Tag)
def delete_tag_handler(sender, instance, **kwargs):
    """Si existe, elimina la imagen del disco."""
    if instance.image and os.path.exists(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_save, sender=models.Resource)
def create_resource_handler(sender, instance, created, **kwargs):
    """Cuando un recurso es creado, menda un ping a google.
    Solo lo manda si DEBUG es False.
    """
    if created and settings.DEBUG is False:
        try:
            ping_google()
        except Exception:
            pass


@receiver(post_delete, sender=models.Resource)
def delete_resource_handler(sender, instance, **kwargs):
    """Si existe, elimina la imagen del disco."""
    if instance.image and os.path.exists(instance.image.path):
        os.remove(instance.image.path)
