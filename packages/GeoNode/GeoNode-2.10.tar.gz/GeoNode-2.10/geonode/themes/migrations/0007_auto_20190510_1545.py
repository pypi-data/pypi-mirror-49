# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-10 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonode_themes', '0006_geonodethemecustomization_body_text_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='geonodethemecustomization',
            name='jumbotron_text_color',
            field=models.CharField(default=b'#ffffff', max_length=10),
        ),
        migrations.AddField(
            model_name='geonodethemecustomization',
            name='jumbotron_title_color',
            field=models.CharField(default=b'#ffffff', max_length=10),
        ),
    ]
