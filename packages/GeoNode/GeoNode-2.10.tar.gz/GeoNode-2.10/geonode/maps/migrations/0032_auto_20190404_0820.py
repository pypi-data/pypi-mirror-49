# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-04 08:20
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0031_auto_20190329_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map',
            options={},
        ),
        migrations.AlterModelManagers(
            name='map',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
