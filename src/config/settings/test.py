# flake8: noqa
from .base import *

# Añadir ~/tests a PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), 'tests'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_*1n=b^@1*a_hov@9__e6&*jt%j2(#+8%+b7-dof$53szmx@=@'

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_django',
        'USER': 'test_django',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Media
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/test')

# Emails

# Email default.
DEFAULT_FROM_EMAIL = 'snicoper@snicoper.com'

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
EMAIL_HOST_PASSWORD = '123456'

# Haystack y Whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
