from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from utils.images import ImageResize
from utils.mixins.models import ImageUpdateModel

from . import settings as accounts_settings
from .managers import UserKarmaManager


class User(ImageUpdateModel, AbstractUser):
    """Model para usuarios."""
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
        blank=True
    )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to=accounts_settings.ACCOUNTS_AVATAR_PATH,
        default='',
        blank=True
    )

    _image_fields = ['avatar']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def save(self, *args, **kwargs):
        """Comprueba si ha añadido o cambiado el avatar."""
        old_avatar = None
        self.slug = slugify(self.username)
        if self.pk:
            old_avatar = User.objects.get(pk=self.pk).avatar
        super().save(*args, **kwargs)
        if not old_avatar and self.avatar:
            self._resize_avatar()
        if self.avatar and old_avatar and self.avatar.path != old_avatar.path:
            self._resize_avatar()

    @property
    def get_avatar(self):
        """Obtener avatar usuario.

        Returns:
            str: Avatar del usuario.

            Si el usuario tiene un avatar, obtendrá el del usuario,
            en caso contrario, el avatar por defecto.
        """
        if not self.avatar or not self.avatar.path:
            return '{}{}/{}'.format(
                settings.MEDIA_URL,
                accounts_settings.ACCOUNTS_AVATAR_PATH,
                accounts_settings.ACCOUNTS_AVATAR_DEFAULT
            )
        return '{}/{}'.format(settings.MEDIA_URL, self.avatar)

    @property
    def get_positives(self):
        """Obtener los votos positivos del usuario."""
        return UserKarma.objects.get_positives_for_user(self)

    @property
    def get_negatives(self):
        """Obtener los votos negativos del usuario."""
        return UserKarma.objects.get_negatives_for_user(self)

    def _resize_avatar(self):
        """Redimensiona el avatar."""
        image_resize = ImageResize(self.avatar.path)
        image_resize.resize(
            save_path=self.avatar.path,
            width=accounts_settings.ACCOUNTS_AVATAR_WIDTH,
            height=accounts_settings.ACCOUNTS_AVATAR_HEIGHT
        )


class UserKarma(models.Model):
    """Karma, votos negativos y positivos de un usuario.

    Una relación de un usuario con otro usuario siempre que se le vote.
    Cuando se crea, siempre se le asigna un voto, positive/negative y
    podrá cambiar el voto siempre que quiera.

    Si cambia el voto de positive a negative (o vice versa), uno incrementa
    en 1 y el otro se establece a 0.

    No instanciar directamente, siempre usar UserKarmaManager para obtener
    los votos como para asignar un negative/positive.
    """
    user_receiver = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_karma_receiver',
        verbose_name='Usuario votado'
    )
    user_vote = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='users_karma_vote',
        verbose_name='Usuario vota'
    )
    positive = models.PositiveSmallIntegerField(
        verbose_name='Positivo',
        blank=True,
        default=0
    )
    negative = models.PositiveSmallIntegerField(
        verbose_name='Negativo',
        blank=True,
        default=0
    )

    objects = UserKarmaManager()

    class Meta:
        verbose_name = 'Karma usuario'
        verbose_name_plural = 'Karma de usuarios'
        unique_together = (('user_receiver', 'user_vote'),)

    def __str__(self):
        return '{}: {}'.format(self.user_receiver.username, self.user_vote.username)
