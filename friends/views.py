from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from friends.relation_strategy import FriendRelation, RequestRelation, FollowingRelation, FollowerRelation
from friends.models import Relation, Request
from friends.serializers import RelationSerializer, FollowerSerializer



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
            elif relation_type == 'follower':
                relation_strategy = FollowerRelation()

            # Do not used
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

        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))
        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '100000'

        # import ipdb;ipdb.set_trace()
        follovers = Relation.objects.raw(
                'SELECT '
                    'friends_follower.id, '
                    'friends_follower.status, '
                    'auth_user.id AS user_pk, '
                    'auth_user.username AS user_name, '
                    'files_profileimage.image AS user_image '

                'FROM friends_follower '
                'LEFT JOIN auth_user ON auth_user.id = friends_follower.friend_id '
                'LEFT JOIN files_profileimage ON auth_user.id = files_profileimage.owner_id '

                'WHERE friends_follower.user = '+str(request.user.pk)+' '

                'ORDER BY auth_user.username ASC '
                'LIMIT '+limit_from+', '+limit_count+''
            )

        serializer = FollowerSerializer(follovers, many=True)
        return Response(serializer.data)


class FollowingsList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))
        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '100000'

        follovings = Relation.objects.raw(
            'SELECT '
                'friends_following.id, '
                'friends_following.status, '
                'auth_user.id AS user_pk, '
                'auth_user.username AS user_name, '
                'files_profileimage.image AS user_image '

            'FROM friends_following '
            'LEFT JOIN auth_user ON auth_user.id = friends_following.friend_id '
            'LEFT JOIN files_profileimage ON auth_user.id = files_profileimage.owner_id '

            'WHERE friends_following.user = ' + str(request.user.pk) + ' '

            'ORDER BY auth_user.username ASC '
            'LIMIT ' + limit_from + ', ' + limit_count + ''
            )

        serializer = FollowerSerializer(follovings, many=True)
        return Response(serializer.data)


class RequestsList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))
        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '100000'

        requests = Relation.objects.raw(
            'SELECT '
            'friends_request.id, '
            'friends_request.status, '
            'auth_user.id AS user_pk, '
            'auth_user.username AS user_name, '
            'files_profileimage.image AS user_image '

            'FROM friends_request '
            'LEFT JOIN auth_user ON auth_user.id = friends_request.friend_id '
            'LEFT JOIN files_profileimage ON auth_user.id = files_profileimage.owner_id '

            'WHERE friends_request.user = ' + str(request.user.pk) + ' '

            'ORDER BY auth_user.username ASC '
            'LIMIT ' + limit_from + ', ' + limit_count + ' '
            )

        serializer = RelationSerializer(requests, many=True)
        return Response(serializer.data)

class RequestsCountView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        requests_count = Request.objects.filter(user=request.user.pk).count()

        return Response({'data': requests_count}, status=status.HTTP_200_OK)