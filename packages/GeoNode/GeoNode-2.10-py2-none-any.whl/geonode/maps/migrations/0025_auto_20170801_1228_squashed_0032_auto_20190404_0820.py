# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-04 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    replaces = [(b'maps', '0025_auto_20170801_1228'), (b'maps', '0026_auto_20180301_1947'), (b'maps', '0027_auto_20180302_0430'), (b'maps', '0028_auto_20180409_1238'), (b'maps', '0029_auto_20180412_0822'), (b'maps', '0030_auto_20180414_2120'), (b'maps', '0031_auto_20190329_1652'), (b'maps', '0032_auto_20190404_0820')]

    dependencies = [
        ('maps', '24_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='abstract_en',
            field=models.TextField(blank=True, help_text='brief narrative summary of the content of the resource(s)', max_length=2000, null=True, verbose_name='abstract'),
        ),
        migrations.AlterField(
            model_name='map',
            name='data_quality_statement_en',
            field=models.TextField(blank=True, help_text="general explanation of the data producer's knowledge about the lineage of a dataset", max_length=2000, null=True, verbose_name='data quality statement'),
        ),
        migrations.AlterField(
            model_name='map',
            name='purpose_en',
            field=models.TextField(blank=True, help_text='summary of the intentions with which the resource(s) was developed', max_length=500, null=True, verbose_name='purpose'),
        ),
        migrations.AlterField(
            model_name='map',
            name='supplemental_information_en',
            field=models.TextField(default='No information provided', help_text='any other descriptive information about the dataset', max_length=2000, null=True, verbose_name='supplemental information'),
        ),
        migrations.AlterModelManagers(
            name='map',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='map',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelManagers(
            name='map',
            managers=[
            ],
        ),
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
