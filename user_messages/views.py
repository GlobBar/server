from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from user_messages.serializers import MessagesSerializer
from user_messages.models import Messages
from rest_framework import status


class MessagesList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        messages = Messages.objects.filter(user_to=request.user.pk)
        messages_serializer = MessagesSerializer(messages, many=True)
        return Response(messages_serializer.data)

    def post(self, request, format=None):
        serializer = MessagesSerializer(data=request.data, context={'current_user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            message = Messages.objects.get(pk=request.data['message_pk'])
        except Messages.DoesNotExist:
            return Response({"data": "message_pk not found!"}, status=status.HTTP_400_BAD_REQUEST)

        message.delete()

        return Response({"data": "message successfully deleted!"}, status=status.HTTP_200_OK)


class MessagesDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, message_pk):
        try:
            message = Messages.objects.get(pk=message_pk)
        except Messages.DoesNotExist:
            return Response({"data": "message_pk not found!"}, status=status.HTTP_404_NOT_FOUND)

        messages_serializer = MessagesSerializer(message)

        return Response(messages_serializer.data)
