from django.conf import settings
from django.db import models

from resources.models import Resource


class Favorite(models.Model):
    """Recursos favoritos de un usuario.

    El campo resources podrá tener 0 o muchos resources como favoritos.

    Se crea con un signal accounts.signals.
    """
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Usuario',
        related_name='favorites_user'
    )
    resources = models.ManyToManyField(
        to=Resource,
        verbose_name='Recursos',
        related_name='favorites_resource',
        blank=True
    )

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return self.user.username
