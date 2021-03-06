from rest_framework import serializers
from report.models import Report, ReportImageLike, UsersWithUnlockedMedia
from django.conf import settings
from django.contrib.auth.models import User
from apiusers.serializers import OwnerSerializer
from apiusers.models import Profile
from files.models import  ReportImage
from places.models import  Place
from report.report_manager import ReportManager
import os
from notification.notification_manager import NotificationManager
from points.points_manager import PointManager


class ReportSerializer(serializers.ModelSerializer):

    report_media = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    price = serializers.IntegerField(required=False)
    is_locked = serializers.SerializerMethodField()

    def get_is_locked(self, obj):
        if obj.is_locked == 0:
            return False

        if obj.user == self.context['request'].user.id or obj.user == self.context['request'].user:
            return False

        try:
            UsersWithUnlockedMedia.objects.get(user=self.context['request'].user, report=obj)

            return False
        except (UsersWithUnlockedMedia.DoesNotExist, Place.DoesNotExist) as e:

            return True

        return True

    def get_is_liked(self, obj):
        try:
            my_like_place_pks = self.context['my_like_report_pks']
        except:
            my_like_place_pks = []

        if str(obj.pk) in my_like_place_pks:
            res = True
        else:
            res = False

        return res


    def get_is_hot(self, obj):
        try:
            like_cnt = obj.reportimagelike_set.count()
            if like_cnt > 19:
                is_hot = True
            else:
                is_hot = False
        except:
            is_hot = False
        return is_hot

    def get_like_cnt(self, obj):
        try:
            like_cnt = obj.reportimagelike_set.count()
        except:
            like_cnt = 0
        return like_cnt

    def get_thumbnail(self, obj):
        try:
            if obj.type == 1:
                thumbnail_path = obj.report_image.image_thumbnail.url
            else:
                thumbnail_path = obj.report_image.thumbnail.url
            res = settings.SITE_DOMAIN
            res += thumbnail_path
        except:
            res = None

        return res

    def to_representation(self, instance):
        report = super(ReportSerializer, self).to_representation(instance)
        for i in report:
            if report[i] is None:
                del report[i]
        return report

    def get_report_media(self, obj):

        if obj.report_image is not None:
            try:
                if obj.type == 1:
                    puth = str(obj.report_image.image)
                else:
                    puth = str(obj.report_image.video)
            except:
                puth = obj.image_from_query
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None
        return res

    def get_created(self, obj):

        if obj.created is not None:
            try:
                res = obj.created.strftime('%Y-%m-%dT%H:%M:%SZ')
            except:
                res = None
        else:
            res = None
        return res


    class Meta:
        model = Report
        fields = ('pk', 'created', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'type', 'report_media', 'description', 'thumbnail', 'like_cnt', 'is_hot',
                  'is_liked','is_locked','price'
                  )

    def save(self, **kwargs):
        report = super(ReportSerializer, self).save(**kwargs)
        user = self.context['request'].user
        try:
            profile = Profile.objects.get(user=user)
            # type1: dancer
            if profile.type == 1:
                report.price = 100
                report.is_locked = True
            else:
                report.price = 0
        except:
            report.price = 0

        report.user = user


        # Set expired date
        report_manager = ReportManager()
        expired_utc = report_manager.get_expired_time(report.place.city)
        report.expired = expired_utc

        report.save()

        # Points
        answer_cnt = 0
        answers = [
            report.is_going,
            report.queue,
            report.charge,
            report.gender_relation,
            report.bar_filling,
            report.music_type,
        ]

        for answ in answers:
            if answ is not None:
                answer_cnt += 1

        point_manager = PointManager()
        #  Add points
        data = {
            'user': report.user,
            'place': report.place,
            'answer_cnt': answer_cnt,  # For each answer user get 1 point
        }
        point_manager.add_point_by_type('answer', data)

        # Send notifications if it is HOT
        notification_manager = NotificationManager()
        notification_manager.send_hot_plases_notify(report)

        return report.save()


class ReportImageLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportImageLike
        fields = ('pk', 'user', 'report')


class ReportForListSerializer(serializers.ModelSerializer):

    report_media = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    price = serializers.IntegerField()
    is_locked = serializers.SerializerMethodField()

    def get_is_locked(self, obj):
        if obj.is_locked == 0:
            return False

        if obj.user == self.context['request'].user.id or obj.user == self.context['request'].user:
            return False

        try:
            UsersWithUnlockedMedia.objects.get(user=self.context['request'].user.id, report=obj.id)

            return False
        except (UsersWithUnlockedMedia.DoesNotExist) as e:

            return True

        return True

    def get_is_liked(self, obj):
        try:
            my_like_place_pks = self.context['my_like_report_pks']
        except:
            my_like_place_pks = []

        if str(obj.pk) in my_like_place_pks:
            res = True
        else:
            res = False

        return res

    def get_is_hot(self, obj):
        like_cnt = 0
        try:
            is_hot = self.context['is_hot']
        except:
            is_hot = False

        if is_hot == True:
            try:
                like_cnt = obj.like_cnt
            except:
                like_cnt = 0

        if like_cnt < 5:
            is_hot = False
        return is_hot

    def get_like_cnt(self, obj):

        try:
            like_cnt = obj.like_cnt
        except:
            like_cnt = 0
        return like_cnt

    def get_thumbnail(self, obj):
        res = None



        if obj.type == 1:
            path = obj.image_from_query
            if path is not None:
                abs_path = settings.MEDIA_ROOT+'/thumbs/'+path
                root_path = 'thumbs/'+path

        else:
            path = obj.thumbnail_from_query
            if path is not None:
                abs_path = settings.MEDIA_ROOT+'/'+path
                root_path = path
                # import ipdb; ipdb.set_trace()

        if path is not None:
            if os.path.isfile(abs_path):
                res = settings.SITE_DOMAIN
                res += '/media/'
                res += root_path

        return res

    def to_representation(self, instance):
        report = super(ReportForListSerializer, self).to_representation(instance)
        for i in report:
            if report[i] is None:
                del report[i]
        return report

    def get_owner(self, obj):

        try:
            user = User.objects.get(pk=obj.user)
            serializer = OwnerSerializer(user)
            return serializer.data
        except:
            return {}

    def get_report_media(self, obj):

        if obj.report_image is not None:


            if obj.type == 1:
                try:
                    puth = str(obj.report_image.image)
                except:
                    puth = obj.image_from_query

            else:
                try:
                    puth = str(obj.report_image.video)
                except:
                    puth = obj.video_from_query


            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None
        return res


    class Meta:
        model = Report
        fields = ('pk', 'created', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'type', 'report_media', 'description', 'owner', 'thumbnail', 'like_cnt', 'is_hot',
                  'is_liked','is_locked','price')
