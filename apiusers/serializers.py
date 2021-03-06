from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from files.models import ProfileImage
from django.conf import settings
import os
from friends.models import Relation, Follower, Following, Request
from points.models import PointsCount
from apiusers.models import Profile

class UserType():
    FAN = 0
    DANCER = 1

    def getUserTypeToArray(self):
        return

class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)
    profile_image = serializers.SerializerMethodField()
    points_count = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
        except Profile.DoesNotExist:
            profile = Profile(type=UserType.FAN, user=obj)
            profile.save()

        type = profile.type
        return type

    def get_points_count(self, obj):
        try:
            point_count = PointsCount.objects.get(user=obj)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=obj)
            point_count.save()

        exist_points = point_count.points
        return exist_points

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        user = User.objects.create(**validated_data)
        passw = self.context['data']
        # import ipdb; ipdb.set_trace()
        if passw is not None:
            user.set_password(passw)
            user.save()
        return user

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


class UserDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)
    profile_image = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    current_relation = serializers.SerializerMethodField()
    points_count = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()


    def get_type(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
        except Profile.DoesNotExist:
            profile = Profile(type=UserType.FAN, user=obj)
            profile.save()

        type = profile.type
        return type

    def get_points_count(self, obj):
        try:
            point_count = PointsCount.objects.get(user=obj)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=obj)
            point_count.save()

        exist_points = point_count.points
        return exist_points

    def get_balance(self, obj):
        try:
            point_count = PointsCount.objects.get(user=obj)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=obj)
            point_count.save()

        balance = point_count.balance
        if balance is None:
            balance = 0
        return balance

    # last_reports = serializers.SerializerMethodField()
    #
    # def get_last_reports(self, obj):
    #     last_reports = Report.objects.filter(user_id=obj.pk, friend_id=obj.pk).order_by('-id')[0:3]
    #     report_seriolaser = ReportForListSerializer(last_reports, many=True)
    #     return report_seriolaser

    def get_followings_count(self, obj):

        followers_cnt = Following.objects.filter(user=obj.pk).count()
        return followers_cnt

    def get_followers_count(self, obj):
        followings_cnt = Follower.objects.filter(user=obj.pk).count()
        return followings_cnt

    def get_current_relation(self, obj):

        current_user = self.context['current_user']
        try:
            is_request = Request.objects.get(user=obj.pk, friend=current_user.pk)
            return 'request'
        except:
            pass

        try:
            is_follower = Follower.objects.get(user=obj.pk, friend=current_user.pk)
            return 'following'
        except:
            pass

        return 'no_relation'

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

class OwnerSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        try:
            # import ipdb; ipdb.set_trace()
            puth = str(obj.profileimage.image)
            is_absolut_puth = puth.find('http')

            if is_absolut_puth == -1:
                my_file = settings.SITE_DOMAIN
                my_file += '/media/'
                my_file += puth
            else:
                my_file = puth

        except :
            anonim = settings.MEDIA_ROOT
            anonim += '/anonim.jpg'
            if os.path.isfile(anonim):
                my_file = settings.SITE_DOMAIN
                my_file += '/media/anonim.jpg'
            else:
                my_file = None

        return my_file

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image')


class LastUsersSerializer(serializers.Serializer):
    pk = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    last_chk_in_created = serializers.SerializerMethodField()
    # user_name = serializers.SerializerMethodField()

    def get_pk(self, obj):
        return obj.user.pk


    def get_last_chk_in_created(self, obj):
        return obj.created

    def get_profile_image(self, obj):
        try:
            profile_image = ProfileImage.objects.get(owner=obj.user)
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


class UserRegisterPassSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    password = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)
    profile_image = serializers.SerializerMethodField()
    points_count = serializers.SerializerMethodField()

    def get_points_count(self, obj):
        try:
            point_count = PointsCount.objects.get(user=obj)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=obj)
            point_count.save()

        exist_points = point_count.points
        return exist_points

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        user = User.objects.create(**validated_data)
        passw = self.context['data']
        # import ipdb; ipdb.set_trace()
        if passw is not None:
            user.set_password(passw)
            user.save()
        return user


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


class UserLoginPassSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, allow_blank=True, max_length=100)
    password = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=250)

class ProfileSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    type = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        profile = super(ProfileSerializer, self).save(**kwargs)
        profile.user = self.context['current_user']

        return profile.save()

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        profile.user = self.context['current_user']
        return profile

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.user = self.context['current_user']
        instance.save()

        return instance

    def validate(self, data):
        if data['type'] not in [UserType.FAN, UserType.DANCER]:
            raise serializers.ValidationError("type in not available")
        return data




