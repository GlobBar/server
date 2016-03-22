from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class PointType(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(null=True, blank=True)
    enable = models.BooleanField(default=True)
    points = models.IntegerField(null=True, blank=True)


class Points(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(default=True)
    points = models.IntegerField(null=True, blank=True)
    type = models.ForeignKey(PointType, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
