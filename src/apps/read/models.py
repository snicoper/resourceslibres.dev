from django.conf import settings
from django.db import models

from resources.models import Resource


class ReadUserResources(models.Model):
    """Recursos marcados como leídos por un usuario.

    Cuando se crea un usuario, src/apps/accounts/signals.py
    creara un objeto ResourcesUserRead para cada usuario.

    Si el usuario lee un recurso se añadira a resources de lo
    contrario no existirá. Si lo tiene marcado como leído y luego
    cambia a no leído, el recurso sera eliminado de resources.
    """
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_read',
        verbose_name='Usuario'
    )
    resources = models.ManyToManyField(
        to=Resource,
        verbose_name='Recursos',
        related_name='resources_read'
    )

    class Meta:
        verbose_name = 'Usuario recursos leído'
        verbose_name_plural = 'Usuario recursos leídos'

    def __str__(self):
        return self.user.username
