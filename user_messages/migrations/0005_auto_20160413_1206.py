# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-13 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0004_auto_20160412_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsmessages',
            options={'ordering': ('id',), 'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
        migrations.AddField(
            model_name='messages',
            name='is_readed',
            field=models.BooleanField(default=False),
        ),
    ]
