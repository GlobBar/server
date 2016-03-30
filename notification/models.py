from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class DevToken(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(default=True)
    is_ios = models.BooleanField(default=True)
    dev_token = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
