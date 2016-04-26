from __future__ import unicode_literals

from django.db import models



class City(models.Model):

    tz_titles = ()

    from pytz import all_timezones
    for zone in all_timezones:
        tz_titles = tz_titles + ((zone, zone),)

    title = models.CharField(max_length=100, blank=False, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    enable = models.BooleanField(default=True)
    time_zone = models.CharField(max_length=100, blank=False, null=True, choices=tz_titles)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=False, null=True)

    def __unicode__(self):
        return u'%s' % (self.title, )

    class Meta:
        ordering = ('title', )
        verbose_name = "City"
        verbose_name_plural = "Cities"
