from rest_framework import serializers
from report.models import Report
from django.conf import settings


class ReportSerializer(serializers.ModelSerializer):

    report_image = serializers.SerializerMethodField()

    def get_report_image(self, obj):

        # import ipdb; ipdb.set_trace()

        if obj.report_image is not None:
            puth = str(obj.report_image.image)
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None

        return res


    class Meta:
        model = Report
        fields = ('pk', 'description', 'place', 'user', 'is_going', 'bar_filling', 'music_type', 'gender_relation',
                  'charge', 'queue', 'place', 'type', 'report_image')

    def save(self, **kwargs):
        report = super(ReportSerializer, self).save(**kwargs)
        report.user = self.context['request'].user

        return report.save()
