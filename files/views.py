from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from files.models import ProfileImage
from rest_framework import status
from apiusers.serializers import UserSerializer
import os
from rest_framework_social_oauth2.views import ConvertTokenView
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
from social.apps.django_app.default.models import UserSocialAuth
import json
import requests


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data['file']
        user_pk = request.data['user_pk']
        # import ipdb; ipdb.set_trace()

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
