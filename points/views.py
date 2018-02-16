from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apiusers.serializers import UserDetailSerializer
from points.models import PointsCount
from points.serializers import PointSerializer
from pytz import timezone
from datetime import datetime
from rest_framework import status


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

