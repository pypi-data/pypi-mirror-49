# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 00:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geonode_client', '0004_auto_20180416_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geonodethemecustomization',
            name='partners',
        ),
        migrations.DeleteModel(
            name='GeoNodeThemeCustomization',
        ),
        migrations.DeleteModel(
            name='Partner',
        ),
    ]
