# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-27 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0006_emailmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='is_sent',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]