# flake8: noqa
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_*1n=b^@1*a_hov@9__e6&*jt%j2(#+8%+b7-dof$53szmx@=@'

ALLOWED_HOSTS = ['resourceslibres.com']

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Sessions
SESSION_COOKIE_DOMAIN = '.resourceslibres.com'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resourceslibrescom',
        'USER': 'resourceslibrescom',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# TEMPLATE CONFIGURATION
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/prod')

# Emails
# Email default.
DEFAULT_FROM_EMAIL = 'webmaster@resourceslibres.com'

# Donde mandara los errores, para mandar emails usar GROUP_EMAILS.
ADMINS = (
    ('Errors and security', 'weberrors@resourceslibres.com'),
)

# Grupos de email.
GROUP_EMAILS = {
    # No reply.
    'NO-REPLY': 'no-responder@snicoper.local <webmaster@resourceslibres.com>',

    # Emails de los administradores.
    'ADMINS': (
        'Salvador Nicolas <snicoper@resourceslibres.com>',
    ),

    # Contacts.
    'CONTACTS': (
        'Salvador Nicolas <snicoper@resourceslibres.com>',
    ),
}

# SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'snicoper@gmail.com'
EMAIL_HOST_PASSWORD = ''

# Haystack y Whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Disqus
DISQUS_SHORTNAME = 'resourceslibres'
