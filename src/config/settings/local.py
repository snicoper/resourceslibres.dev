# flake8: noqa
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*h-nj!a*9r74ael028l53*u$5299g5k)kzaw@0+@e920+@-owh'

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.100', 'resourceslibres.local']

INTERNAL_IPS = ['127.0.0.1']

# Application definition
THIRD_PARTY_APPS += (
    'debug_toolbar',
    'django_extensions',
)

LOCAL_APPS += (
    'home.apps.HomeConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resourceslibresdev',
        'USER': 'snicoper',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/local')

# Emails

# Email default.
DEFAULT_FROM_EMAIL = 'snicoper@snicoper.local'

# Donde mandara los errores, para mandar emails usar GROUP_EMAILS.
ADMINS = (
    ('Errors and security', 'snicoper@snicoper.local'),
)

# Grupos de email.
GROUP_EMAILS = {
    # No reply.
    'NO-REPLY': 'no-responder@snicoper.local <snicoper@snicoper.local>',

    # Emails de los administradores.
    'ADMINS': (
        'Salvador Nicolas <snicoper@snicoper.local>',
    ),

    # Contacts.
    'CONTACTS': (
        'Salvador Nicolas <snicoper@snicoper.local>',
    ),
}

# SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.snicoper.local'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'snicoper'
EMAIL_HOST_PASSWORD = ''

# Haystack y Whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Mostrar fake adsense? muestra unas imagenes en su lugar.
ADSENSE_IMAGES_FAKE = True

# Django 1.11 los forms Select multiple relentiza mucho, desactivar estos paneles.
DEBUG_TOOLBAR_CONFIG = {
   # Add in this line to disable the panel
    'DISABLE_PANELS': {
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    },
}
