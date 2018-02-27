from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Type of points and count of balls
class PointType(models.Model):
    title = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(null=True, blank=True)
    enable = models.BooleanField(default=True)
    points_count = models.IntegerField(null=True, blank=True)
    points_count_partner = models.IntegerField(null=True, blank=True)

# Points history
class Points(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(default=True)
    points = models.IntegerField(null=True, blank=True)
    type = models.ForeignKey(PointType, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

# Points count by users
class PointsCount(models.Model):
    updated = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(default=True)
    points = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

# FeeSize
class FeeSize(models.Model):
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0,)

# Transactions
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    finance_email = models.CharField(max_length=200, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_success = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)


