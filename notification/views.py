from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from notification.models import DevToken
from rest_framework import status
from pushy.models import Device
from notification_manager import NotificationManager
from django.conf import settings
import random, string

class NotificationList(APIView):


    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        dev_token_str = request.POST.get('dev_token')

        try:
            exist_device = Device.objects.get(user=user)
            exist_device.key = dev_token_str
            exist_device.save()
        except Device.DoesNotExist:
            Device.objects.create(key=dev_token_str, type=Device.DEVICE_TYPE_IOS, user=user)

        return Response({'data': 'Token was successfully added.'})

    def delete(self, request, format=None):
        user = request.user
        try:
            dev_token = Device.objects.get(user=user)
            dev_token.delete()
        except Device.DoesNotExist:
            return Response({'data': 'Can\'t remove dev_token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': 'Token was successfully deleted.'})

    def put(self, request, format=None):
        user = request.user

        try:
            device = Device.objects.get(user=user)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Get notification strategy
        notification_sender = NotificationManager().get_notification_strategy(device)
        notification_sender.set_device_token(device.key).set_data({'test': 'Hello world!'}).send_message()

        # import socket, ssl, json, struct
        # import binascii
        #
        # deviceToken = str(device.key)
        #
        # thePayLoad = {
        #      'aps': {
        #           'alert': 'Hello world Taranka :)',
        #           'sound': 'bingbong.aiff',
        #           'badge': 42
        #           },
        #      'test_data': {'foo': 'bar'},
        #      }
        #
        # # theCertfile = '/var/www/html/nightlife/notification/test.pem'
        # theCertfile = settings.PEM_KEY_DIR
        #
        # theHost = ( 'gateway.sandbox.push.apple.com', 2195 )
        #
        # data = json.dumps( thePayLoad )
        #
        # deviceToken = deviceToken.replace(' ','')
        #
        # byteToken = binascii.unhexlify(deviceToken)
        #
        # theFormat = '!BH32sH%ds' % len(data)
        #
        # theNotification = struct.pack( theFormat, 0, 32,
        #
        # byteToken, len(data), data )
        #
        # ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = theCertfile )
        #
        # ssl_sock.connect( theHost )
        #
        # ssl_sock.write( theNotification )
        #
        # ssl_sock.close()

        return Response({'data': 'Token was successfully SENT.'})



class MailSending(APIView):

    def post(self, request, format=None):
        import sendgrid
        from django.template import loader

        # APIkey
        sg = sendgrid.SendGridClient(settings.SEND_GRID_API_KEY)

        ran_str = ''.join(random.choice(string.lowercase) for i in range(20))

        context = {
            'userName': 'testUser',
            'ran_str': ran_str,
        }

        body_html = loader.get_template('notification/emails/test_email.html').render(context)

        message = sendgrid.Mail(to=['ermine.kostya@gmail.com', 'ermine.kostya1@gmail.com'], subject='Example', html=body_html, text='Body',
                                from_email='doe@email.com')
        status, msg = sg.send(message)
        # print(status, msg)

        return Response(body_html)