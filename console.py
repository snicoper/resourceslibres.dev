#!/usr/bin/env python
# flake8: noqa
# Para pruebas rapidas

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.local')

import django
django.setup()

############################################################################
from accounts.models import User, UserKarma

snicoper = User.objects.get(pk=1)
snicoper2 = User.objects.get(pk=1)
perico = User.objects.get(pk=2)

print(snicoper == snicoper2)
