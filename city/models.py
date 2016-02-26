from __future__ import unicode_literals

from django.db import models


class City(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    enable = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.title, )

    class Meta:
        ordering = ('title', )
