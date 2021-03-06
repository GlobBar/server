# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 13:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('enable', models.BooleanField(default=True)),
                ('points', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PointType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('enable', models.BooleanField(default=True)),
                ('points_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='points',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='points.PointType'),
        ),
        migrations.AddField(
            model_name='points',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
