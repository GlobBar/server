# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devtoken',
            name='dev_token',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]