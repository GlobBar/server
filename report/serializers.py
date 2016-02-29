from rest_framework import serializers
from report.models import Report, ReportImageLike
from django.conf import settings


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

    # def get_is_going(self, obj):
    #     if self.context['request'].data['is_going'] is not None:
    #         return self.context['request'].data['is_going']
    #     return None
    #
    # def get_bar_filling(self, obj):
    #     if self.context['request'].data['bar_filling'] is not None:
    #         return self.context['request'].data['bar_filling']
    #     return None
    #
    # def get_music_type(self, obj):
    #     if self.context['request'].data['music_type'] is not None:
    #         return self.context['request'].data['music_type']
    #     return None
    #
    # def get_gender_relation(self, obj):
    #     if self.context['request'].data['gender_relation'] is not None:
    #         return self.context['request'].data['gender_relation']
    #     return None
    #
    # def get_charge(self, obj):
    #     if self.context['request'].data['charge'] is not None:
    #         return self.context['request'].data['charge']
    #     return None
    #
    # def get_queue(self, obj):
    #     try:
    #         if self.context['request'].data['queue'] is not None:
    #             return self.context['request'].data['queue']
    #     except:
    #         pass

        # return None


    class Meta:
        model = Report
        fields = ('pk', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'type', 'report_image')

    def save(self, **kwargs):
        report = super(ReportSerializer, self).save(**kwargs)
        report.user = self.context['request'].user

        return report.save()


class ReportImageLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportImageLike
        fields = ('pk', 'user', 'report')
