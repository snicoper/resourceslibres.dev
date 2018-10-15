from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from favorites.models import Favorite
from read.models import ReadUserResources


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_handler(sender, instance, created, **kwargs):
    """Al crear un usuario creara:

        favoritos asociados al usuario,
        recursos leídos por el usuario.
    """
    if not created:
        return
    Favorite.objects.create(user=instance)
    ReadUserResources.objects.create(user=instance)
