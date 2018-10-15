# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-03 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0006_resourceformat'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='resource_format',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resource_format', to='resources.ResourceFormat', verbose_name='Format'),
            preserve_default=False,
        ),
    ]
