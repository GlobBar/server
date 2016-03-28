# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 10:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('points', '0002_pointtype_points_count_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointsCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('enable', models.BooleanField(default=True)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
