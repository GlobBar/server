from rest_framework import serializers
from points.models import PointsCount


class PointSerializer(serializers.ModelSerializer):

    # expired = serializers.SerializerMethodField()
    #
    # def get_expired(self, obj):
    #     pass

    class Meta:
        model = PointsCount
        fields = ('pk', 'points', 'enable')
