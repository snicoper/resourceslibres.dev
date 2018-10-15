import inspect

from django.db import models

from resources import settings as resources_settings
from utils.images import ImageResize


class IconImageMixin(models.Model):
    """Al añadir o cambiar una imagen, la redimensiona.

    Requiere que el campo del modelo sea MyModel.image del tipo ImageField.
    El ancho y alto lo obtiene de ICON_IMAGE_WIDTH y ICON_IMAGE_HEIGHT,
    en src/apps/resources/settings.py.

    En caso de añadir el mixin src/apps/utils/mixins/models.ImageUpdateModel,
    añadirlo antes de ImageUpdateModel.

        class MyClass(IconImageMixin, ImageUpdateModel, models.Model):
            # ...
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Si añade o cambia la imagen, se redimensiona.

        Obtiene la clase del modelo dinamicamente.
        """
        module = inspect.getmodule(self)
        klass = getattr(module, self.__class__.__name__)
        old_image_path = False

        if self.pk:
            instance = klass.objects.get(pk=self.pk)
            if instance.image:
                old_image_path = instance.image.path
        super().save(*args, **kwargs)
        if old_image_path and old_image_path != self.image.path or self.image:
            resize = ImageResize(self.image.path)
            resize.resize(
                self.image.path,
                width=resources_settings.ICON_IMAGE_WIDTH,
                height=resources_settings.ICON_IMAGE_HEIGHT
            )
