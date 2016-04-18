from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class FbTokenToPost(models.Model):
    token = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
