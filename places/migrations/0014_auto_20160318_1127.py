# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-18 11:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_auto_20160315_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='expired',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 18, 23, 59, 59)),
        ),
    ]