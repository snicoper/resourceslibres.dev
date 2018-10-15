from django.conf import settings
from django.db import models
from django.urls import reverse

from utils.images import ImageResize
from utils.mixins.models import ImageUpdateModel, SlugFieldModel

from . import settings as resources_settings
from .managers import RatioManager, ResourceManager
from .mixins.models import IconImageMixin


class ResourceFormat(IconImageMixin, ImageUpdateModel, models.Model):
    """Formatos del resource, video, lectura, etc."""
    title = models.CharField(
        verbose_name='Formato',
        unique=True,
        max_length=100
    )
    image = models.ImageField(
        upload_to='resources/formats',
        verbose_name='Imagen'
    )

    class Meta:
        verbose_name = 'Formato'
        verbose_name_plural = 'Formatos'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Category(IconImageMixin, ImageUpdateModel, SlugFieldModel, models.Model):
    """Categorías para los recursos."""
    image = models.ImageField(
        upload_to='resources/categories',
        verbose_name='Imagen'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ('title',)


class Language(ImageUpdateModel, SlugFieldModel, models.Model):
    """Idiomas de los recursos."""
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Código',
        help_text='https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'
    )
    flag = models.ImageField(
        upload_to='resources/languages',
        verbose_name='Bandera'
    )

    _image_fields = ['flag']

    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'
        ordering = ('-code',)


class Tag(IconImageMixin, ImageUpdateModel, SlugFieldModel, models.Model):
    """Etiquetas/Lenguajes de los recursos."""
    image = models.ImageField(
        upload_to='resources/tags',
        verbose_name='Imagen'
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ('title',)


class Resource(ImageUpdateModel, SlugFieldModel, models.Model):
    """Recursos del sitio."""
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='resource_owner'
    )
    categories = models.ManyToManyField(
        to=Category,
        verbose_name='Categorías',
        related_name='resource_categories'
    )
    main_tag = models.ForeignKey(
        to=Tag,
        on_delete=models.CASCADE,
        verbose_name='Etiqueta principal',
        related_name='resource_main_tag',
        null=True
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Etiquetas',
        related_name='resource_tags',
    )
    resource_format = models.ForeignKey(
        to=ResourceFormat,
        on_delete=models.CASCADE,
        verbose_name='Formato',
        related_name='resource_format'
    )
    languages = models.ManyToManyField(
        to=Language,
        verbose_name='Idiomas',
        related_name='resource_languages'
    )
    link = models.URLField(
        verbose_name='Enlace'
    )
    image = models.ImageField(
        upload_to='resources/resources',
        verbose_name='Imagen',
        blank=True,
        default=''
    )
    description = models.TextField(
        verbose_name='Descripcción',
        help_text=(
            '<a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet"'
            'target="_blank">Markdown</a> permitido'
        )
    )
    require_register = models.BooleanField(
        verbose_name='Requiere registro',
        default=False,
        blank=True
    )
    views = models.IntegerField(
        verbose_name='Visitas',
        default=0
    )
    clicks = models.IntegerField(
        verbose_name='Clicks enlace',
        default=0
    )
    marked_broken = models.PositiveIntegerField(
        verbose_name='Marcados como rotos',
        default=0,
        blank=True
    )
    marked_spam = models.PositiveIntegerField(
        verbose_name='Marcados como spam',
        default=0,
        blank=True
    )
    active = models.BooleanField(
        verbose_name='Activo',
        default=False
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha publicación'
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultima actualización'
    )

    objects = ResourceManager()

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ('-create_at',)

    def save(self, *args, **kwargs):
        """Si añade o cambia la imagen, se redimensiona."""
        old_image_path = False
        if self.pk:
            old_image = Resource.objects.get(pk=self.pk)
            if old_image.image:
                old_image_path = old_image.image.path
        super().save(*args, **kwargs)
        if old_image_path and old_image_path != self.image.path or self.image:
            resize = ImageResize(self.image.path)
            resize.resize(
                self.image.path,
                width=resources_settings.RESOURCE_IMAGE_WIDTH,
                height=resources_settings.RESOURCE_IMAGE_HEIGHT
            )

    def get_absolute_url(self):
        return reverse('resources:details', kwargs={'slug': self.slug})

    def get_ratio(self):
        """Obtener el ratio del recurso.

        Returns:
            float: Ratio medio del recurso.
        """
        ratio = self.ratio_resource.aggregate(models.Avg('score'))
        if ratio['score__avg']:
            return ratio['score__avg']
        return 0

    def get_image(self):
        """Obtener la imagen que representa el recurso.

        Si no tiene una en self.image, se obtendrá la imagen de self.main_tag.image.
        """
        return self.image if self.image else self.main_tag.image


class Ratio(models.Model):
    """Puntuaciones de los recursos."""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='ratio_user'
    )
    resource = models.ForeignKey(
        to=Resource,
        on_delete=models.CASCADE,
        verbose_name='Recursos',
        related_name='ratio_resource'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Puntuación'
    )

    objects = RatioManager()

    class Meta:
        verbose_name = 'Ratio'
        verbose_name_plural = 'Ratios'
        unique_together = (('user', 'resource'),)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.resource.title)


class QuickResource(SlugFieldModel, models.Model):
    """Un recurso temporal simple de un usuario.

    Se crea de manera temporal para mas tarde el superuser poder crear
    las categorías y etiquetas que falten.

    Solo guarda el owner y el link.
    """
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='quick_resource_owner'
    )
    link = models.URLField(
        verbose_name='Enlace'
    )
    message = models.TextField(
        verbose_name='Mensaje',
        help_text='Añade cualquier sugerencia',
        blank=True,
        default=''
    )
    create_at = models.DateTimeField(
        verbose_name='Creado el',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Recurso rápido'
        verbose_name_plural = 'Recursos rápidos'
        ordering = ('-create_at',)

    def __str__(self):
        return '{}: {}'.format(self.owner.username, self.link)
