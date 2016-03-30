from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from notification.models import DevToken
from rest_framework import status
from pushy.models import Device
from pushy.utils import send_push_notification


class NotificationList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        dev_token_str = request.POST.get('dev_token')


        Device.objects.create(key=dev_token_str, type=Device.DEVICE_TYPE_IOS, user=user)




        # if dev_token_str is None:
        #     return Response({'data': 'Invalid dev_token.'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # try:
        #     dev_token = DevToken.objects.get(user=user)
        #     dev_token.dev_token = dev_token_str
        # except DevToken.DoesNotExist:
        #     dev_token = DevToken(
        #         user=user,
        #         dev_token=dev_token_str,
        #     )
        #
        # dev_token.save()






        return Response({'data': 'Token was successfully added.'})

    def delete(self, request, format=None):
        user = request.user
        try:
            dev_token = DevToken.objects.get(user=user)
            dev_token.delete()
        except DevToken.DoesNotExist:
            return Response({'data': 'Can\'t remove dev_token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': 'Token was successfully deleted.'})

    def put(self, request, format=None):
        user = request.user
        device = Device.objects.get(user=user)
        send_push_notification('YOUR TITLE', {'msg': 'test'}, device=device)

        return Response({'data': 'Token was successfully SEND.'})
