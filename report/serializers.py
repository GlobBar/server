from rest_framework import serializers
from report.models import Report, ReportImageLike
from django.conf import settings
from django.contrib.auth.models import User
from apiusers.serializers import OwnerSerializer


class ReportSerializer(serializers.ModelSerializer):

    report_image = serializers.SerializerMethodField()

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


    class Meta:
        model = Report
        fields = ('pk', 'created', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'type', 'report_image'
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

    def to_representation(self, instance):
        report = super(ReportForListSerializer, self).to_representation(instance)
        for i in report:
            if report[i] is None:
                del report[i]
        return report

    def get_owner(self, obj):
        # import ipdb;ipdb.set_trace()

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
                  'charge', 'queue', 'type', 'report_image'
                  , 'owner'
                  )
