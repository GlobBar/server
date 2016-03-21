from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit import ImageSpec, register


class ProfileImage(models.Model):
    image = models.FileField(upload_to='profile/%Y/%m/%d')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class ReportImage(models.Model):
    image = models.FileField(upload_to='report/%Y/%m/%d')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image_thumbnail = ImageSpecField(source='image', id='images:thumb_',)

class ThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(300, 300)]
    format = 'JPEG'
    options = {'quality': 70}

    # put thumbnails into the "photos/thumbs" folder and
    # name them the same as the source file
    @property
    def cachefile_name(self):
        source_filename = getattr(self.source, 'name', None)
        s = "thumbs/" + source_filename
        return s

register.generator('images:thumb_', ThumbnailSpec)
