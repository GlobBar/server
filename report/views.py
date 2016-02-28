from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from report.serializers import ReportSerializer, ReportImageLikeSerializer
from report.models import ReportImageLike


class ReportList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportImageLikeDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        report_pk = request.data.get('report')
        report_like = ReportImageLike.objects.filter(report_id=report_pk, user=request.user).first()

        # Create just one like for user in this report
        if report_like is None:
            request.data.update({'user': request.user.pk})
            serializer = ReportImageLikeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReportImageLikeSerializer(report_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
