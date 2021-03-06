from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from report.serializers import ReportSerializer, ReportImageLikeSerializer, ReportForListSerializer
from report.models import ReportImageLike, Report
from places.models import Place, Checkin, Like
from city.models import City
from datetime import datetime
import pytz, os
from report.report_repository import ReportRepository
from django.conf import settings


class ReportList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,  format=None):
        pk = request.GET.get('report_pk')
        report = self.get_object(pk)
        # if is video /image
        video = 2
        img = 1

        if report.report_image is not None:
            # Remove files
            file = report.report_image
            if report.type == video:
                pathes = [
                    settings.MEDIA_ROOT+'/'+str(file.video),
                    settings.MEDIA_ROOT+'/'+str(file.thumbnail)
                    ]
            elif report.type == img:
                pathes = [
                    settings.MEDIA_ROOT+'/'+str(file.image),
                    settings.MEDIA_ROOT+'/thumbs/'+str(file.image)
                ]

            # Remove likes
            likes = ReportImageLike.objects.filter(report=report)
            if likes.count() > 0:
                for li in likes:
                    li.delete()

            file.delete()

            for path in pathes:
                if os.path.isfile(path):
                    os.remove(path)

        report.delete()

        return Response({"data": "Report was successfully deleted."}, status=status.HTTP_200_OK)


class ReportDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        # My likes
        my_like_report_pks = []
        my_likes = ReportImageLike.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_report_pks += [str(i.report.pk)]

        snippet = self.get_object(pk)
        serializer = ReportSerializer(snippet, context={'my_like_report_pks': my_like_report_pks, 'request': request})
        return Response(serializer.data)



class ReportImageLikeDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        report_pk = request.POST.get('report_pk')
        report_like = ReportImageLike.objects.filter(report_id=report_pk, user=request.user).first()

        # Create just one like for user in this report
        if report_like is None:
            req_data = {'user': request.user.pk, 'report': report_pk}
            serializer = ReportImageLikeSerializer(data=req_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReportImageLikeSerializer(report_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Get Today reports
class ReportsByPeriod(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user_id = request.user
        pk = None
        city_pk = str(request.GET.get('filter_city'))
        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))

        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '9'

        # My likes
        my_like_report_pks = []
        my_likes = ReportImageLike.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_report_pks += [str(i.report.pk)]

        my_checin = Checkin.objects.filter(user=request.user, active=True).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        try:
            city = City.objects.get(pk=city_pk)
            zone_title = city.time_zone
            # TimeZone hours delta
            tz_delta_dirty = datetime.now(pytz.timezone(zone_title)).strftime('%z')
        except:
            zone_title = 'America/Indiana/Indianapolis'
            # TimeZone hours delta
            tz_delta_dirty = datetime.now(pytz.timezone(zone_title)).strftime('%z')

        if len(tz_delta_dirty) == 5:
            start = tz_delta_dirty
            finish = tz_delta_dirty
            tz_delta = start[0:3]+':'+finish[3:]
        else:
            tz_delta = '+00:00'

        frt = '%Y-%m-%d 06:00:00'

        reportRepoinst = ReportRepository()

        # TODAY
        if str(request.GET.get('period_filter')) == 'today':
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'frt': frt, 'city_pk': city_pk}
            hot_reports = ReportRepository.getTodayReportsHot(reportRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta,
                          'str_pk': str_pk,
                          'correct_limit_from': correct_limit_from,
                          'correct_limit_count': correct_limit_count,
                          'city_pk': city_pk,
                          'frt': frt
                          }
            simple_reports = ReportRepository.getTodayReports(reportRepoinst, parameters)

        # WEEK
        elif str(request.GET.get('period_filter')) == 'week':
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'frt': frt, 'city_pk': city_pk}
            hot_reports = ReportRepository.getWeekReportsHot(reportRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta,
                          'str_pk': str_pk,
                          'correct_limit_from': correct_limit_from,
                          'correct_limit_count': correct_limit_count,
                          'city_pk': city_pk,
                          'frt': frt
                          }
            simple_reports = ReportRepository.getWeekReports(reportRepoinst, parameters)

        # MONTH
        elif str(request.GET.get('period_filter')) == 'month':
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'frt': frt, 'city_pk': city_pk}
            hot_reports = ReportRepository.getMonthReportsHot(reportRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta,
                          'str_pk': str_pk,
                          'correct_limit_from': correct_limit_from,
                          'correct_limit_count': correct_limit_count,
                          'city_pk': city_pk,
                          'frt': frt
                          }
            simple_reports = ReportRepository.getMonthReports(reportRepoinst, parameters)

        else:
            return Response('Parameter period_filter  incorrect or not found', status=status.HTTP_400_BAD_REQUEST)

        # IF limit_from > hot_count => Hot_places does not view
        if (correct_limit_from + hot_count) > hot_count:
            hot_reports_result = []
        else:
            hot_reports_result = serializer_hot_reports.data
        serializer_simple_reports = ReportForListSerializer(simple_reports, many=True, context={'my_like_report_pks': my_like_report_pks, 'request': request})

        return Response({
             'reports': hot_reports_result + serializer_simple_reports.data
        })

    def correctionLimitFrom(self, limit_from, hot_count):
        if limit_from == 'None' or limit_from == '0':
            limit_from = int(hot_count)
        elif int(limit_from) <= hot_count:
            raise Http404
        else:
            limit_from = int(limit_from)

        correct_limit_from = limit_from - hot_count

        return correct_limit_from

    def correctionLimitCount(self, limit_from, limit_count, hot_count):
        if limit_count == 'None':
            limit_count = 9
        else:
            limit_count = int(limit_count)

        if int(limit_from) > 3:
            # If not first page -> do not minus hot_count
            correct_limit_count = limit_count
        else:
            # If first page -> minus hot_count
            correct_limit_count = limit_count - hot_count

        return correct_limit_count

    def getHotData(self, serializer_hot_reports):
        str_ = ',0'
        hot_count = 0
        for i in serializer_hot_reports.data:
            hot_count +=1
            str_ = str_+','+str(i.get('pk'))

        str_pk = '('+str_[1:]+')'

        return {'hot_count': hot_count, 'str_pk': str_pk}



