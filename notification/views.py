from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class NotificationList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):



        return Response({'data': 'Successfully add token'})

    def delete(self, request, format=None):

        return Response({'data': 'Successfully delete token'})
