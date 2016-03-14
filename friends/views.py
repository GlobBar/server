from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from friends.relation_strategy import FriendRelation, RequestRelation, FollowingRelation
from friends.models import Relation
from friends.serializers import RelationSerializer



class RelationList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):

        is_create = None
        relation_type = False

        # Check request

        if request.POST.get('friend_pk') == 'None':
            return Response({'error': 'parameter friend_pk not found'}, status=status.HTTP_400_BAD_REQUEST)

        if request.POST.get('relation_type') == 'None':
            return Response({'error': 'parameter relation_type not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            relation_type = request.POST.get('relation_type')

        if 'is_create' in request.POST:
            if str(request.POST.get('is_create')) == 'true':
                is_create = True

        # Get friend - user

        try:
            friend = User.objects.get(pk=request.POST.get('friend_pk'))

            # Get strategy

            if relation_type == 'request':
                relation_strategy = RequestRelation()
            elif relation_type == 'following':
                relation_strategy = FollowingRelation()
            elif relation_type == 'friend':
                relation_strategy = FriendRelation()
            else:
                 return Response({'error': 'Invalid relation_type'}, status=status.HTTP_400_BAD_REQUEST)

            # Create relation

            if is_create is None:
                relation_strategy.remove_relation(request.user, friend)
            else:
                relation_strategy.create_relation(request.user, friend)

        except User.DoesNotExist:
            return Response({'error': 'Invalid friend_pk'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': 'Relation successfully created/removed.'}, status=status.HTTP_201_CREATED)


class FollowerList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        checkin = Relation.objects.all()


        serializer = RelationSerializer(checkin, many=True)
        return Response(serializer.data)

