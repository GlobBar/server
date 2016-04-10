# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 06:03
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
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_from', models.IntegerField(blank=True, null=True)),
                ('body', models.TextField()),
                ('status', models.IntegerField(blank=True, null=True)),
                ('is_pushed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]