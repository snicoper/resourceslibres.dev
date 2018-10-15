from django.conf import settings

# Ancho del avatar.
ACCOUNTS_AVATAR_WIDTH = getattr(settings, 'ACCOUNTS_AVATAR_WIDTH', 100)

# Alto del avatar.
ACCOUNTS_AVATAR_HEIGHT = getattr(settings, 'ACCOUNTS_AVATAR_HEIGHT', 100)

# Avatar path.
ACCOUNTS_AVATAR_PATH = getattr(settings, 'ACCOUNTS_AVATAR_PATH', 'accounts/profiles')

# Default avatar.
ACCOUNTS_AVATAR_DEFAULT = getattr(settings, 'ACCOUNTS_AVATAR_DEFAULT', 'anonymous.png')
