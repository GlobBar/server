from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    user = models.IntegerField(null=True, blank=True)
    friend = models.ForeignKey(User,  null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)


class Request(models.Model):
    user = models.IntegerField(null=True, blank=True)
    friend = models.ForeignKey(User,  null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    status = models.IntegerField(null=True, blank=True, default=0)


class Following(models.Model):
    user = models.IntegerField(null=True, blank=True)
    friend = models.ForeignKey(User,  null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    status = models.IntegerField(null=True, blank=True, default=0)


class Follower(models.Model):
    user = models.IntegerField(null=True, blank=True)
    friend = models.ForeignKey(User,  null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    status = models.IntegerField(null=True, blank=True, default=0)


