from rest_framework import serializers
from user_messages.models import Messages
from django.contrib.auth.models import User
from apiusers.serializers import OwnerSerializer


class MessagesSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ('pk', 'title', 'body', 'user_from', 'user_to', 'owner', 'created', 'is_readed')

    def save(self, **kwargs):
        message = super(MessagesSerializer, self).save(**kwargs)
        message.user_from = self.context['current_user']

        return message.save()

    def get_owner(self, obj):

        try:
            user = User.objects.get(pk=obj.user_from.pk)
            serializer = OwnerSerializer(user)
            return serializer.data
        except:
            return {}

