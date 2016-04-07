from rest_framework import serializers
from messages.models import Messages


class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = ('pk', 'body', 'user_from_pk',)



