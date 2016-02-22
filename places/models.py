from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Place(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField()
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', )


class Checkin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id', )
