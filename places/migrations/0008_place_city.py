# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0001_initial'),
        ('places', '0007_checkin_is_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.City'),
        ),
    ]
