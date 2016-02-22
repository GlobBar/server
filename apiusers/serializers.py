from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from files.models import ProfileImage
from django.conf import settings
import os

class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)
    profile_image = serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance

    def get_profile_image(self, obj):
        try:
            profile_image = ProfileImage.objects.get(owner=obj)
            puth = str(profile_image.image)
            is_absolut_puth = puth.find('http')

            if is_absolut_puth == -1:
                my_file = settings.SITE_DOMAIN
                my_file += '/media/'
                my_file += puth
            else:
                my_file = puth

        except ProfileImage.DoesNotExist:
            anonim = settings.MEDIA_ROOT
            anonim += '/anonim.jpg'
            if os.path.isfile(anonim):
                my_file = settings.SITE_DOMAIN
                my_file += '/media/anonim.jpg'
            else:
                my_file = None

        return my_file


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
