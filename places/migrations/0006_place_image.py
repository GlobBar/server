# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20160224_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='place/%Y/%m/%d'),
        ),
    ]
