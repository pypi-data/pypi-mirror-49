# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-16 02:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geonode_themes', '0002_auto_20181015_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geonodethemecustomization',
            name='identifier',
        ),
    ]
