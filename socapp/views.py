from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from socapp.models import FbTokenToPost
import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings


class FbPosts(APIView):
    # auth
    permission_classes = (permissions.IsAuthenticated,)

    # FbPosts
    def post(self, request, format=None):
        err = False
        stat_code = status.HTTP_201_CREATED
        user = request.user
        try:
            user_fb_access_token = FbTokenToPost.objects.get(user=user)
        except FbTokenToPost.DoesNotExist:
            err = 'invalid token'
            stat_code = status.HTTP_400_BAD_REQUEST

        if err is False:
            puth = '/media/logo_100.jpg'
            logo = settings.SITE_DOMAIN
            logo += puth

            final_url = "https://graph.facebook.com/me/feed"
            params = {
                'message': 'Nightlife',
                'access_token': user_fb_access_token.token,
                'description': "Check out the GlobBar app! We bar hoppers help each other out and earn points towards discounted drinks.",
                'link': 'https://itunes.apple.com',
                'picture': logo
                }
            res = requests.post(final_url, data=params)
            if res.status_code != 200:
                err = 'invalid token'
                stat_code = status.HTTP_400_BAD_REQUEST

        if err is False:
            err = 'successfully sent fb post'

        return Response({'data': err}, status=stat_code)

    # Refresh FbPosts token
    def put(self, request, format=None):
        user = request.user
        fresh_token = request.POST.get('fb_token')
        try:
            user_fb_access_token = FbTokenToPost.objects.get(user=user)
        except FbTokenToPost.DoesNotExist:
            user_fb_access_token = FbTokenToPost(user=user)

        user_fb_access_token.token = fresh_token
        user_fb_access_token.save()

        return Response({'data': 'Token successfully updated!'}, status=status.HTTP_201_CREATED)
