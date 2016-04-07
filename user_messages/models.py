from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):
    user_to = models.IntegerField(null=True, blank=True)
    user_from = models.ForeignKey(User,  null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

