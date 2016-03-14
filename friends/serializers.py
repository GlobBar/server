from rest_framework import serializers
from friends.models import Relation


class RelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = ('pk', 'user', 'friend', 'status')



