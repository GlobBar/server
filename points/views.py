from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from apiusers.serializers import UserDetailSerializer
from points.models import PointsCount
from points.serializers import PointSerializer
from pytz import timezone
from datetime import datetime
from rest_framework import status
from django.http import Http404
from user_messages.models import Messages


class PointsList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        point_serializer = PointSerializer(point_count)

        return Response(point_serializer.data)

    def post(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        # Update points
        exist_points = point_count.points
        spent_points_data = request.POST.get('spent_points')
        if spent_points_data == 'None':
            spent_points = 0
        else:
            spent_points = int(spent_points_data)

        if spent_points > exist_points:
            return Response({'error': ('You try to spent more points then you have !')}, status=status.HTTP_400_BAD_REQUEST)

        now_utc = datetime.now(timezone('UTC'))
        updated_points = exist_points - spent_points
        point_count.points = updated_points
        point_count.updated = now_utc
        point_count.save()

        point_serializer = PointSerializer(point_count)

        return Response(point_serializer.data)

class BalanceUp(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=request.user)
            point_count.save()

        # Update balance
        exist_balance = point_count.balance
        if exist_balance is None:
            exist_balance = 0
        balance_delta = request.POST.get('balance_delta')

        now_utc = datetime.now(timezone('UTC'))
        updated_balance = exist_balance + int(balance_delta)
        point_count.points = 0
        point_count.balance = updated_balance
        point_count.updated = now_utc
        point_count.save()

        user_serializer = UserDetailSerializer(request.user)

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)



class BalanceDonate(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        current_user = request.user

        try:
            user = User.objects.get(pk=request.POST.get('pk'))
        except User.DoesNotExist:
            raise Http404

        if current_user.id == user.id:
            return Response({'error': ('You try to donate your self !')}, status=status.HTTP_400_BAD_REQUEST)

        balance_delta = int(request.POST.get('amount'))

        current_user_point_count = self.poin_count_by_user(current_user)
        point_count = self.poin_count_by_user(user)
        if balance_delta > current_user_point_count.balance:
            return Response({'error': ('You try to spent more maney then you have !')}, status=status.HTTP_400_BAD_REQUEST)

        # Update balance
        now_utc = datetime.now(timezone('UTC'))
        point_count.balance = point_count.balance + balance_delta
        point_count.updated = now_utc
        point_count.save()

        current_user_point_count.balance = current_user_point_count.balance - balance_delta
        current_user_point_count.updated = now_utc
        current_user_point_count.save()

        # Creating Message
        body = current_user.username+' donated you '+str(float(balance_delta)/100)+'$'
        message = Messages(title='Balance update', body=body, user_from=current_user, user_to=user.id, created=now_utc, is_readed=0)
        message.save()

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)

    def poin_count_by_user(self, user):
        try:
            point_count = PointsCount.objects.get(user=user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=user)
            point_count.save()

        return point_count
