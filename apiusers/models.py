from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from places.models import Place


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True
    )
    place = models.OneToOneField(
        Place,
        null=True
    )
    type = models.IntegerField(null=True, blank=True) # type1: dancer , 0: fun