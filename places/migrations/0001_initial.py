# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('address', models.CharField(blank=True, default='', max_length=250)),
                ('description', models.TextField()),
                ('enable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
