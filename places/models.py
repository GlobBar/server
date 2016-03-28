from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from city.models import City
from datetime import datetime, timedelta


class Place(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_lst_rpt = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, default='')
    opening_hours = models.CharField(max_length=100, blank=True, default='')
    music_type = models.CharField(max_length=100, blank=True, default='')
    age_group = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField()
    enable = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    image = models.FileField(upload_to='place/%Y/%m/%d', blank=True, null=True)
    logo = models.FileField(upload_to='place_logo/%Y/%m/%d', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id', )


class Checkin(models.Model):

    now = datetime.now()
    expired_time = now.replace(hour=23, minute=59, second=59, microsecond=0)

    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField(default=expired_time)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', )


class Like(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id', )



