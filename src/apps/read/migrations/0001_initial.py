# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-02-27 18:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadUserResources',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_read', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('resources', models.ManyToManyField(related_name='resources_read', to='resources.Resource', verbose_name='Recursos')),
            ],
            options={
                'verbose_name': 'Usuario recursos leído',
                'verbose_name_plural': 'Usuario recursos leídos',
            },
        ),
    ]