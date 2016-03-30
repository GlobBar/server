# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 11:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0015_auto_20160323_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='is_partner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='expired',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 28, 23, 59, 59)),
        ),
    ]