# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-25 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0026_auto_20160413_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.FileField(help_text='JPEG images only', null=True, upload_to='place/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='place',
            name='logo',
            field=models.FileField(help_text='JPEG images only', null=True, upload_to='place_logo/%Y/%m/%d'),
        ),
    ]
