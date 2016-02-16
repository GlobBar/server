from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        # instance.title = validated_data.get('title', instance.title)
        # instance.address = validated_data.get('address', instance.address)
        # instance.description = validated_data.get('description', instance.description)
        # instance.enable = validated_data.get('enable', instance.enable)

        instance.save()
        return instance


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
