# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-05 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faabrickmap_data', '0009_auto_20200305_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='societe',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Ville'),
        ),
    ]
