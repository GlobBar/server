# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-25 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiusers', '0002_auto_20190509_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='place',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='places.Place'),
        ),
    ]
