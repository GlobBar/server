from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from files.models import ProfileImage, ReportImage
from rest_framework import status
from apiusers.serializers import UserSerializer
import os
from rest_framework_social_oauth2.views import ConvertTokenView
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
from social.apps.django_app.default.models import UserSocialAuth
import json
import requests
from report.models import Report
from report.serializers import ReportSerializer
from report.report_manager import ReportManager
from places.models import Place
from notification.notification_manager import NotificationManager


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file']
        user_pk = request.data['user_pk']

        try:
            user = User.objects.get(id=user_pk)
        except User.DoesNotExist:
            return Response({'pk': ('Invalid pk')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profileimage = ProfileImage.objects.get(owner=user)

            # remove old file
            import os.path
            myfile = settings.MEDIA_ROOT
            myfile += '/'
            myfile += str(profileimage.image)

            if os.path.isfile(myfile):
                os.remove(myfile)

            profileimage.image = file_obj

        except ProfileImage.DoesNotExist:
            profileimage = ProfileImage(image=file_obj, owner=user, )

        profileimage.save()
        self.id = profileimage.id

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class ReportFileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file']
        place_pk = request.data['place_pk']

        try:
           description = request.data['description']
        except:
           description = None
        user = request.user

        try:
            place = Place.objects.get(id=place_pk)
        except Place.DoesNotExist:
            return Response({'pk': ('Invalid pk')}, status=status.HTTP_400_BAD_REQUEST)

        report_image = ReportImage(image=file_obj, owner=user, )

        report_image.save()
        self.id = report_image.id

        report = Report(
            description=description,
            type=1,  # (0 - report, 1 - picture)
            user=user,
            place=place,
            report_image=report_image
        )
        report.save()

        # Set expired date
        report_manager = ReportManager()
        expired_utc = report_manager.get_expired_time(report)
        report.expired = expired_utc

        report.save()

        # Send notifications if it is HOT
        notification_manager = NotificationManager()
        notification_manager.send_hot_plases_notify(report)

        serializer = ReportSerializer(report, many=False)

        return Response(serializer.data)

    # Update report (image and video)
    def put(self, request, format = None):
        description = request.POST.get('description')
        current_user = request.user
        try:
            report = Report.objects.get(pk=request.POST.get('report_pk'))
            report_owner = report.user
        except Report.DoesNotExist:
            return Response({'data': 'Invalid pk, report not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if description != 'None' and current_user.pk == report_owner.pk:
            report.description = description
            report.save()

        serializer = ReportSerializer(report, many=False)
        return Response(serializer.data)


class ConvertTokenViewCustom(ConvertTokenView):
    def post(self, request, *args, **kwargs):

        res = super(ConvertTokenViewCustom, self).post(request, *args, **kwargs)

        anonim = settings.MEDIA_ROOT
        anonim += '/anonim.jpg'
        if os.path.isfile(anonim):
            profile_picture_url = 'anonim.jpg'
        else:
            profile_picture_url = None

        try:
            acc_token = json.loads(res.content)['access_token']
        except :
            return res

        user = AccessToken.objects.get(token=acc_token).user
        user_soc_auth = UserSocialAuth.objects.get(user=user)

        backend = request.POST['backend']

        if backend == 'instagram':
            # Set instagram Token manually
            try:
                user_soc_auth.extra_data['access_token'] = request.POST['token']
                user_soc_auth.save()
            except:
                pass

            path = 'https://api.instagram.com/v1/users/'+user_soc_auth.uid+'/?access_token='+user_soc_auth.extra_data['access_token']
            try:
                url = requests.get(path).json()['data']['profile_picture']
                profile_picture_url = url
            except:
                pass

        elif backend == 'facebook':
            try:
                url ='http://graph.facebook.com/'+user_soc_auth.uid+'/picture?type=large'
                profile_picture_url = url
            except:
                pass
        try:
            # If avatar already exist do nothing
            profileimage = ProfileImage.objects.get(owner=user)

        except ProfileImage.DoesNotExist:
            # Else create avatar from sicial
            profileimage = ProfileImage(owner=user)
            profileimage.image = profile_picture_url
            profileimage.save()

        return res
