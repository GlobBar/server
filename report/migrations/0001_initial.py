# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 13:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0002_reportimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0004_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('enable', models.BooleanField(default=True)),
                ('is_going', models.BooleanField()),
                ('bar_filling', models.IntegerField()),
                ('music_type', models.IntegerField()),
                ('gender_relation', models.IntegerField()),
                ('charge', models.IntegerField()),
                ('queue', models.IntegerField()),
                ('type', models.IntegerField(default=0)),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='places.Place')),
                ('report_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.ReportImage')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
