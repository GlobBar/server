from __future__ import unicode_literals
from django.db import models


class Place(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField()
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', )
