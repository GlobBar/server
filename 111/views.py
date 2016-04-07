from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from points.models import PointsCount
from messages.serializers import MessagesSerializer
from rest_framework import status


class MessagesList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        point_serializer = MessagesSerializer(point_count)

        return Response(point_serializer.data)

    def post(self, request, format=None):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        point_serializer = MessagesSerializer(point_count)

        return Response(point_serializer.data)
