# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_reportimagelike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='bar_filling',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='charge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='gender_relation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_going',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='music_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='queue',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]