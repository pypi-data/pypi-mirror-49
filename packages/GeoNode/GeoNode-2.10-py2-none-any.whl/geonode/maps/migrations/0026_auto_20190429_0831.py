# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 08:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0025_auto_20170801_1228_squashed_0032_auto_20190404_0820'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelManagers(
            name='map',
            managers=[
            ],
        ),
    ]
