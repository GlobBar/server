from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class DeviceToken(models.Model):

    token = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ('id', )
