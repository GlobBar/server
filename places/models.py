from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from city.models import City
from datetime import datetime, timedelta


class Place(models.Model):

    #describing
    title = models.CharField(max_length=100, blank=False, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField()

    #metadata
    opening_hours = models.CharField(max_length=100, blank=True, default='')
    music_type = models.CharField(max_length=100, blank=True, default='')
    age_group = models.CharField(max_length=100, blank=True, default='')

    #assets
    image = models.FileField(upload_to='place/%Y/%m/%d', blank=False, null=True, help_text='JPEG images only')
    logo = models.FileField(upload_to='place_logo/%Y/%m/%d', blank=False, null=True, help_text='JPEG images only')

    #date related
    created = models.DateTimeField(auto_now_add=True)
    last_push_expired = models.DateTimeField(auto_now_add=True)
    created_lst_rpt = models.DateTimeField(blank=True, null=True)

    #booleans
    enable = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)

    #location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=False, null=True)

    #foreign keys
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=False)

    def clean(self):
        import re
        from django.core.exceptions import ValidationError

        p = re.compile(r'.*\.(jpg|jpeg)$', re.I)
        filename = self.image.name
        if not p.match(filename):
            raise ValidationError('You must upload a JPEG image')

    class Meta:
        ordering = ('id', )
        verbose_name = "Venue"
        verbose_name_plural = "Venues List"

    def __unicode__(self):
        return u'%s' % (self.title, )


class Checkin(models.Model):

    # now = datetime.now()
    # expired_time = now.replace(hour=23, minute=59, second=59, microsecond=0)

    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', )


class Like(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('id', )



