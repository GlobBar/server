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
        is_dublicate_name = False

        try:
            file_obj = request.data['file']
        except:
            file_obj = None

        try:
            user_name = request.data['user_name']
        except:
            user_name = None


        user_pk = request.data['user_pk']


        try:
            # user = User.objects.get(id=user_pk)
            user = request.user
        except User.DoesNotExist:
            return Response({'pk': ('Invalid pk')}, status=status.HTTP_400_BAD_REQUEST)



        try:
            profileimage = ProfileImage.objects.get(owner=user)

            if file_obj is not None:
                # remove old file
                import os.path
                myfile = settings.MEDIA_ROOT
                myfile += '/'
                myfile += str(profileimage.image)

                if os.path.isfile(myfile):
                    os.remove(myfile)
                profileimage.image = file_obj

            # Check name duplication
            users_same_name = User.objects.filter(username=user_name).exclude(pk=user.pk)
            # import ipdb;ipdb.set_trace()
            if users_same_name.count() > 0:
                is_dublicate_name = True

            if user_name is not None and is_dublicate_name is False:
                user.username = user_name
                user.save()

        except ProfileImage.DoesNotExist:
            profileimage = ProfileImage(image=file_obj, owner=user, )
            if user_name is not None:
                user.username = user_name
                user.save()


        profileimage.save()
        self.id = profileimage.id

        serializer = UserSerializer(user, many=False)

        if is_dublicate_name is True:
            return Response({'data': 'Name duplication'}, status=status.HTTP_200_OK)

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
            type=1,  # (0 - report, 1 - picture, 2 - video)
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

    # Update report (image)
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



class ReportVideoUploadView(APIView):
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
           thumb_video_obj = request.data['thumbnail']
        except:
           thumb_video_obj = None
        user = request.user

        try:
            place = Place.objects.get(id=place_pk)
        except Place.DoesNotExist:
            return Response({'pk': ('Invalid pk')}, status=status.HTTP_400_BAD_REQUEST)

        report_image = ReportImage(
            video=file_obj,
            owner=user,
            thumbnail=thumb_video_obj,
        )

        report_image.save()
        self.id = report_image.id

        report = Report(
            description=description,
            type=2,  # (0 - report, 1 - picture, 2 - video)
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

    # Update report (video)
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


"""""""""
VIDEO RANGE
"""""""""
#
# class ReportVideoRangeView(APIView):
#     parser_classes = (MultiPartParser,)
#
#     def get(self, request, format=None):
#         # sourse_ = settings.MEDIA_ROOT + settings.VIDEO_TEST
#         #
#         # with open(sourse_, 'rb') as f:
#         #     data = f.read()
#         #
#         # lenth = len(data)
#
#         import urllib2
#         conn = urllib2.urlopen('http://127.0.0.1:8000/media/report/2016/04/07/SampleVideo_1280x720_1mb.mp4')
#         byte = conn.read()
#         conn.close()
#         lenth = len(byte)
#
#
#          # get range
#         r = request.META["HTTP_RANGE"]
#         start = int(r.replace("bytes=", "").split("-")[0])
#         finish = int(r.replace("bytes=", "").split("-")[1])
#
#         # start_o = start + offset
#
#
#         range_data = byte[start:finish]
#         # import ipdb;ipdb.set_trace()
#
#         response = Response(range_data, content_type="video/mp4", status=206)
#         response['Accept-Ranges'] = 'bytes'
#         response['Accept-Content-Length'] = lenth
#         # response['Connection'] = 'keep-alive'
#         response['Content-Range'] = 'bytes '+str(start)+'-'+str(finish)+'/'+str(lenth)
#
#         return response
#
#
#     def head(self, request, format=None):
#         # f = open(settings.MEDIA_ROOT + '/report/2016/04/07/SampleVideo_1280x720_1mb.mp4')
#         # data = f.read()[0:10]
#
#         response = Response( content_type="video/mp4", status=206)
#         response['Accept-Ranges'] = 'bytes'
#         response['Accept-Content-Length'] = '1000'
#         # response['X-Accel-Redirect'] = settings.MEDIA_URL + 'report/2016/03/23/SampleVideo_1280x720_1mb.mp4'
#
#
#         return response

class ReportVideoRangeView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):


        return Response('TEST')
