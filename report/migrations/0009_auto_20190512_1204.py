# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-12 12:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0008_auto_20160412_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersWithUnlockedMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='is_locked',
            field=models.NullBooleanField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='price',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AddField(
            model_name='userswithunlockedmedia',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='report.Report'),
        ),
        migrations.AddField(
            model_name='userswithunlockedmedia',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
