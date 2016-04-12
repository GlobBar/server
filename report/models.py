from __future__ import unicode_literals
from django.db import models
from places.models import Place
from city.models import City
from files.models import ReportImage
from django.contrib.auth.models import User


class Report(models.Model):


    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    enable = models.BooleanField(default=True)
    is_going = models.NullBooleanField(null=True, blank=True)
    bar_filling = models.IntegerField(null=True, blank=True)
    music_type = models.IntegerField(null=True, blank=True)
    gender_relation = models.IntegerField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    queue = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=0)  # 0 - report, 1 - picture
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    report_image = models.ForeignKey(ReportImage, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name = "Report"
        verbose_name_plural = "Added Reports"

class ReportImageLike(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id',)
