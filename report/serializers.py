from rest_framework import serializers
from report.models import Report, ReportImageLike
from django.conf import settings
from django.contrib.auth.models import User
from apiusers.serializers import OwnerSerializer
from files.models import  ReportImage
import os

class ReportSerializer(serializers.ModelSerializer):

    report_image = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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
            thumbnail_path = obj.report_image.image_thumbnail.url
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

    def get_report_image(self, obj):

        if obj.report_image is not None:
            try:
                puth = str(obj.report_image.image)
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
                  'charge', 'queue', 'type', 'report_image', 'description', 'thumbnail', 'like_cnt', 'is_hot',
                  'is_liked'
                  )

    def save(self, **kwargs):
        report = super(ReportSerializer, self).save(**kwargs)
        report.user = self.context['request'].user

        return report.save()


class ReportImageLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportImageLike
        fields = ('pk', 'user', 'report')


class ReportForListSerializer(serializers.ModelSerializer):

    report_image = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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

        if like_cnt < 2:
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

        path = obj.image_from_query
        if path is not None:
            abs_path = settings.MEDIA_ROOT+'/thumbs/'+path
            if os.path.isfile(abs_path):
                res = settings.SITE_DOMAIN
                res += '/media/thumbs/'
                res += path
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

    def get_report_image(self, obj):

        if obj.report_image is not None:
            try:
                puth = str(obj.report_image.image)
            except:
                puth = obj.image_from_query
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None
        return res


    class Meta:
        model = Report
        fields = ('pk', 'created', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'type', 'report_image', 'description', 'owner', 'thumbnail', 'like_cnt', 'is_hot',
                  'is_liked')
