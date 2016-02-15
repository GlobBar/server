from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apiusers.serializers import UserSerializer, GroupSerializer
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # auth
    permission_classes = (permissions.IsAuthenticated,)

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # auth
    permission_classes = (permissions.IsAuthenticated,)
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
