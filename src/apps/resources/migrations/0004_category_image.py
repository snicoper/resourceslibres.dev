# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-02 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_auto_20170301_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='resources/tags', verbose_name='Imagen'),
            preserve_default=False,
        ),
    ]