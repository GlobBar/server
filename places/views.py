from places.models import Place, Checkin, Like
from places.serializers import PlaceSerializer, CheckinSerializer, LikeSerializer, PlaceDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from city.models import City
from city.serializers import CitySerializer
from report.serializers import ReportSerializer
from datetime import datetime
import pytz


class SnippetList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        limitFrom = str(request.GET.get('limit_from'))
        limitCount = str(request.GET.get('limit_count'))

        latitude = str(request.GET.get('latitude'))
        longitude = str(request.GET.get('longitude'))

        filter_city = str(request.GET.get('filter_city'))

        if limitFrom == 'None':
            limitFrom = '0'
        if limitCount == 'None':
            limitCount = '100000'

        if latitude == 'None':
            return Response({'error': ('Invalid or missing perameter latitude in u request')}, status=status.HTTP_400_BAD_REQUEST)
        if longitude == 'None':
            return Response({'error': ('Invalid or missing perameter longitude in u request')}, status=status.HTTP_400_BAD_REQUEST)

        if filter_city == 'None':
            my_city_pk = False
        else:
            try:
                my_city_pk = ' WHERE places_place.city_id = '+str(City.objects.get(pk=filter_city).pk)
            except:
                my_city_pk = False

        # if city pk does not pass from client - find most nearest cities pk
        if my_city_pk is False:
            my_city = City.objects.raw(
                'SELECT '
                    'city_city.id '
                'FROM city_city '
                'WHERE city_city.enable = 1 '
                'ORDER BY ROUND(( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( latitude ) ) * '
                    'cos( radians( longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                    '* sin( radians( latitude ) ) ) ) * 1000 / 1609.34, 1) '
                    '  ASC '
                'LIMIT 0, 1'
            )
            try:
                my_city_pk = ' WHERE places_place.city_id = '+str(my_city[0].pk)
            except IndexError:
                my_city_pk = ''


        places = Place.objects.raw(
            'SELECT '
                'places_place.id , '
                'places_place.title, '
                'places_place.address, '
                'places_place.description, '
                'places_place.enable, '
                'places_place.created, '
                'places_place.created_lst_rpt, '
                'places_place.latitude, '
                'places_place.longitude, '
                'ROUND(( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( latitude ) ) * '
                'cos( radians( longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                '* sin( radians( latitude ) ) ) ) * 1000 / 1609.34, 1) '
                'AS distance, '
                'COUNT(ch.id) as checkin_cnt, '
                'COUNT(l.id) as like_cnt '

            'FROM places_place '
            'LEFT JOIN places_checkin ch ON ch.place_id = places_place.id '
            'LEFT JOIN places_like l ON l.place_id = places_place.id '

            ' '+my_city_pk+' '
            'GROUP BY places_place.id '
            'ORDER BY places_place.created_lst_rpt DESC, distance ASC '


            'LIMIT '+limitFrom+', '+limitCount+''
        )
        my_checin = Checkin.objects.filter(user=request.user).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        serializer = PlaceSerializer(places, many=True, context={'my_check_in': my_check_in})

        cities = City.objects.filter(enable=1)
        city_serializer = CitySerializer(cities, many=True)
        data = {'places': serializer.data, 'cities': city_serializer.data}

        return Response(data)

    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))

        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '9'

        my_checin = Checkin.objects.filter(user=request.user).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk
        # import ipdb;ipdb.set_trace()

        try:
            place = Place.objects.get(pk=pk)
            zone_title = place.city.time_zone
        except:
            zone_title = 'America/Indiana/Indianapolis'

        tz_delta_dirty = datetime.now(pytz.timezone(zone_title)).strftime('%z')
        if len(tz_delta_dirty) == 5:
            start = tz_delta_dirty
            finish = tz_delta_dirty
            tz_delta = start[0:3]+':'+finish[3:]
        else:
            tz_delta = '+00:00'

        frt = '%Y-%m-%d 06:00:00'



        # MONTH
        # Hot
        if str(request.GET.get('period_filter')) == 'month':
            hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*30) HOUR, %s) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk,  frt)
            )

            serializer_hgot_reports = ReportSerializer(hot_reports, many=True)

            # Remove duplicates
            hot_data = self.getHotData(serializer_hgot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)


             # Simple

            simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*30) HOUR, %s) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt)
            )


        elif str(request.GET.get('period_filter')) == 'week':
            # WEEK
            hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND (CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*7) HOUR, %s)) '
                'AND (CONVERT_TZ(report_report.created,\'+00:04\', \''+tz_delta+'\') < DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*6) HOUR, %s)) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk, frt, frt)
            )

            serializer_hgot_reports = ReportSerializer(hot_reports, many=True)

            # Remove duplicates
            hot_data = self.getHotData(serializer_hgot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND (CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*7) HOUR, %s)) '
                 'AND (CONVERT_TZ(report_report.created,\'+00:04\', \''+tz_delta+'\') < DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL (6+24*6) HOUR, %s)) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt, frt)
            )


        else:
                # TODAY
            hot_reports = Place.objects.raw(
                'SELECT '
                    'report_report.id , '
                    'report_report.created , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                'FROM report_report '
                'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                'GROUP BY report_report.id '
                'ORDER BY like_cnt DESC , report_report.created  DESC '
                'LIMIT 0,3'
                , (pk, frt)
            )

            serializer_hgot_reports = ReportSerializer(hot_reports, many=True)

            # Remove duplicates
            hot_data = self.getHotData(serializer_hgot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            simple_reports = Place.objects.raw(
                 'SELECT '
                    'report_report.id , '
                    'report_report.description , '
                    'report_report.place_id AS place, '
                    'report_report.user_id AS user, '
                    'report_report.report_image_id AS report_image, '
                    'report_report.is_going , '
                    'report_report.bar_filling , '
                    'report_report.music_type , '
                    'report_report.gender_relation , '
                    'report_report.charge , '
                    'report_report.queue , '
                    'report_report.type , '
                    'report_report.created , '
                    'ri.image AS image_from_query, '
                    'COUNT(l.id) as like_cnt '
                 'FROM report_report '
                 'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
                 'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
                 'WHERE report_report.place_id = %s AND report_report.enable = 1 '
                 'AND CONVERT_TZ(report_report.created,\'+00:00\', \''+tz_delta+'\') > DATE_FORMAT(CONVERT_TZ(NOW(),\'+00:00\', \''+tz_delta+'\') - INTERVAL 6 HOUR, %s) '
                 'AND report_report.id NOT IN '+str_pk+' '
                 'GROUP BY report_report.id '
                 'ORDER BY report_report.created  DESC '
                 'LIMIT '+str(correct_limit_from)+', '+str(correct_limit_count)
                 , (pk, frt)
            )

        # IF limit_from > hot_count => Hot_places does not view
        if (correct_limit_from + hot_count) > hot_count:
            hot_reports_result = []
        else:
            hot_reports_result = serializer_hgot_reports.data
        # import ipdb;ipdb.set_trace()
        serializer_simple_reports = ReportSerializer(simple_reports, many=True)

        place = self.get_object(pk)
        serializer_place = PlaceDetailSerializer(place, context={'my_check_in': my_check_in})


        return Response({
            'place': serializer_place.data
            , 'reports': hot_reports_result + serializer_simple_reports.data
            , 'field_for_testing(simple_pl)': serializer_simple_reports.data
                         })

    def put(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = self.get_object(pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def correctionLimitFrom(self, limit_from, hot_count):
        if limit_from == 'None' or limit_from == '0':
            limit_from = int(hot_count)
        elif int(limit_from) <= hot_count:
            # raise Response({'error': 'Invalid parameter limit_from. It mast be > 3'}, status=status.HTTP_400_BAD_REQUEST)
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

    def getHotData(self, serializer_hgot_reports):
        str_ = ',0'
        hot_count = 0
        for i in serializer_hgot_reports.data:
            hot_count +=1
            str_ = str_+','+str(i.get('pk'))

        str_pk = '('+str_[1:]+')'

        return {'hot_count': hot_count, 'str_pk': str_pk}



class CheckinList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        checkin = Checkin.objects.all()
        serializer = CheckinSerializer(checkin, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        checkin = Checkin.objects.filter(user=request.user).first()

        if checkin is None:
            request.data.update({'user': request.user.pk, 'place': request.POST.get('place_pk')})
            serializer = CheckinSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            try:
                place = Place.objects.get(pk=request.POST.get('place_pk'))
            except Place.DoesNotExist:
                return Response({'error': 'Invalid place_pk'}, status=status.HTTP_400_BAD_REQUEST)
            checkin.place = place
            # import ipdb; ipdb.set_trace()
            if 'is_hidden' in request.POST:
                if str(request.POST.get('is_hidden')) == 'true':
                    checkin.is_hidden = True
                else:
                    checkin.is_hidden = False

            checkin.save()
            serializer = CheckinSerializer(checkin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        like = Like.objects.all()
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        place_id = request.POST.get('place_pk')
        user_id = request.user.id
        like = Like.objects.filter(place_id=place_id, user=request.user).first()
        # Create just one like for user in this place
        if like is None:
            request.data.update({'user': user_id, 'place': place_id})
            serializer = LikeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'pk': str(like.pk), 'place': str(place_id), 'user': str(user_id)}, status=status.HTTP_201_CREATED)



