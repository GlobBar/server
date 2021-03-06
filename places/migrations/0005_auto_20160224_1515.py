# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='created_lst_rpt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
    ]
