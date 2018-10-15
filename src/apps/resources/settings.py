from django.conf import settings

# Ancho imagen Resource.
RESOURCE_IMAGE_WIDTH = getattr(settings, 'RESOURCE_IMAGE_WIDTH', 250)

# Alto imagen Resource.
RESOURCE_IMAGE_HEIGHT = getattr(settings, 'RESOURCE_IMAGE_HEIGHT', 250)

# Ancho imagenes de iconos.
ICON_IMAGE_WIDTH = getattr(settings, 'TAG_IMAGE_WIDTH', 150)

# Alto imagenes de iconos.
ICON_IMAGE_HEIGHT = getattr(settings, 'TAG_IMAGE_HEIGHT', 150)
