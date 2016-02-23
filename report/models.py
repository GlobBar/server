from __future__ import unicode_literals
from django.db import models
from places.models import Place
from files.models import ReportImage
from django.contrib.auth.models import User


class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    enable = models.BooleanField(default=True)
    is_going = models.BooleanField()
    bar_filling = models.IntegerField()
    music_type = models.IntegerField()
    gender_relation = models.IntegerField()
    charge = models.IntegerField()
    queue = models.IntegerField()
    type = models.IntegerField(default=0)  # 0 - report, 1 - picture
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    report_image = models.ForeignKey(ReportImage, on_delete=models.CASCADE, null=True, blank=True)

