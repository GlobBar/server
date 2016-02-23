from django.db import models
from django.contrib.auth.models import User


class ProfileImage(models.Model):
    image = models.FileField(upload_to='profile/%Y/%m/%d')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class ReportImage(models.Model):
    image = models.FileField(upload_to='report/%Y/%m/%d')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
