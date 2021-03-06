from places.models import Place, Checkin, Like
from places.serializers import PlaceSerializer, CheckinSerializer, LikeSerializer, PlaceDetailSerializer
from places.place_repository import PlaceRepository
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from city.models import City
from city.serializers import CitySerializer
from report.serializers import ReportForListSerializer
from report.models import ReportImageLike
import pytz
from points.points_manager import PointManager
from notification.notification_manager import NotificationManager
from pytz import timezone
from datetime import datetime, timedelta

from django.db.models import Count, Min, Sum, Avg
from report.models import Report
from apiusers.models import Profile
from report.report_manager import ReportManager

class SnippetList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user_id = str(request.user.pk)

        limitFrom = str(request.GET.get('limit_from'))
        limitCount = str(request.GET.get('limit_count'))
        if limitFrom == 'None':
            limitFrom = '0'
        if limitCount == 'None':
            limitCount = '100000'


        latitude = str(request.GET.get('latitude'))
        longitude = str(request.GET.get('longitude'))

        filter_city = str(request.GET.get('filter_city'))

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
                ' SELECT '
                    'city_city.id, '
                    'COUNT(places_place.id) AS cnt '
                ' FROM city_city '
                ' LEFT JOIN places_place  ON places_place.city_id = city_city.id'
                ' WHERE city_city.enable = 1 '
                ' GROUP BY city_city.id '
                ' HAVING cnt > 0 '
                ' ORDER BY ROUND(( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( city_city.latitude ) ) * '
                    'cos( radians( city_city.longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                    '* sin( radians( city_city.latitude ) ) ) ) * 1000 / 1609.34, 1) '
                    '  ASC '
                ' LIMIT 0, 1'
            )
            try:
                my_city_pk = ' WHERE places_place.city_id = '+str(my_city[0].pk)
            except IndexError:
                my_city_pk = ''


        places = Place.objects.raw(
            'SELECT '
                'places_place.id , '
                'places_place.city_id , '
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
                'AS distance '

            'FROM places_place '
            ' '+my_city_pk+' '
            'GROUP BY places_place.id '
            'ORDER BY places_place.created_lst_rpt DESC, distance ASC '
            'LIMIT '+limitFrom+', '+limitCount+''
        )

        # My likes
        my_like_place_pks = []
        my_likes = Like.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_place_pks += [str(i.place.pk)]

        # My check ins
        my_checin = Checkin.objects.filter(user=request.user, active=True).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        serializer = PlaceSerializer(places, many=True, context={
            'my_check_in': my_check_in,
            'my_check_in_entity': my_checin,
            'my_like_place_pks': my_like_place_pks
        })

        # cities = City.objects.filter(enable=1)
        # city_serializer = CitySerializer(cities, many=True)

        data = {'places': serializer.data
                # ,'cities': city_serializer.data
                }

        return Response(data)

    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VenueListView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        limitFrom = str(0)#str(request.GET.get('limit_from'))
        limitCount = str(100)#str(request.GET.get('limit_count'))

        latitude = str(request.GET.get('latitude'))
        longitude = str(request.GET.get('longitude'))
        filter_city = request.GET.get('city_id')

        if (latitude == 'None') or (longitude == 'None'):
            return Response({'error': ('Missing coordinates in request')}, status=status.HTTP_400_BAD_REQUEST)

        if (filter_city == 'None'):
            return Response({'error': ('Missing city reference in request')}, status=status.HTTP_400_BAD_REQUEST)

        #topPlace

        city = City.objects.get(pk=filter_city)
        if city is None:
            return Response({'error': ('Missing invalid city id')}, status=status.HTTP_400_BAD_REQUEST)

        manager = ReportManager()
        today_end = manager.get_expired_time(city)
        today_start = today_end - timedelta(days=1)

        #one club should be on top of the list
        #this club has most reports for today
        #in case 2 clubs have equal amount => hot is the one that got most reports earlier
        #in case no reports left => no club is the top
        maybe_top_club = Place.objects\
            .filter(city_id=filter_city)\
            .filter(report__created__range=[today_start,today_end])\
            .annotate(reportsNumber=Count('report'))\
            .order_by('-reportsNumber', 'created_lst_rpt')\
            .first()

        filter_top_query = ''
        if maybe_top_club is not None:
            filter_top_query = 'AND places_place.id <> '+str(maybe_top_club.pk)

        places = Place.objects.raw(
            'SELECT '
                'places_place.id , '
                'places_place.city_id , '
                'places_place.title, '
                'places_place.address, '
                'places_place.description, '
                'places_place.enable, '
                'places_place.created, '
                'places_place.created_lst_rpt, '
                'places_place.latitude, '
                'places_place.longitude, '
                '( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( latitude ) ) * '
                'cos( radians( longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                '* sin( radians( latitude ) ) ) ) * 1000 '
                'AS distance '

            'FROM places_place '
            'WHERE places_place.city_id = '+str(filter_city)+' '+filter_top_query+' '
            'GROUP BY places_place.id '
            'ORDER BY distance ASC '
            'LIMIT '+limitFrom+', '+limitCount+''
        )

        if maybe_top_club:
            places = [maybe_top_club] + list(places)

        # My likes
        my_like_place_pks = []
        my_likes = Like.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_place_pks += [str(i.place.pk)]

        # My check ins
        my_checin = Checkin.objects.filter(user=request.user, active=True).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        serializer = PlaceSerializer(places, many=True, context={
            'my_check_in': my_check_in,
            'my_check_in_entity': my_check_in ,
            'my_like_place_pks': my_like_place_pks
        })

        return Response({ 'places': serializer.data })

class NearestSnippetList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        limitFrom = str(request.GET.get('limit_from'))
        limitCount = str(request.GET.get('limit_count'))

        latitude = str(request.GET.get('latitude'))
        longitude = str(request.GET.get('longitude'))

        if limitFrom == 'None':
            limitFrom = '0'
        if limitCount == 'None':
            limitCount = '10'

        if latitude == 'None':
            return Response({'error': ('Invalid or missing perameter latitude in u request')}, status=status.HTTP_400_BAD_REQUEST)
        if longitude == 'None':
            return Response({'error': ('Invalid or missing perameter longitude in u request')}, status=status.HTTP_400_BAD_REQUEST)

        places = Place.objects.raw(
            'SELECT '
                'places_place.id , '
                'places_place.city_id , '
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
                '* sin( radians( latitude ) ) ) ) * 1000 / 1609.34, 2) '
                'AS distance '

            'FROM places_place '
            'ORDER BY distance ASC '
            'LIMIT '+limitFrom+', '+limitCount+''
        )

        serializer = PlaceSerializer(places, many=True, context={})
        data = {'places': serializer.data}
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
        if pk == 'me':
            try:
                profile = Profile.objects.get(user=request.user)
                pk = profile.place.id
            except:
                raise Http404

        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))

        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '9'

        # My Report likes
        my_like_report_pks = []
        my_likes_report = ReportImageLike.objects.filter(user=request.user)
        if my_likes_report.count() > 0:
            for l in my_likes_report:
                my_like_report_pks += [str(l.report.pk)]

        # My Place likes
        my_like_place_pks = []
        my_likes = Like.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_place_pks += [str(i.place.pk)]

        # My Check ins
        my_checin = Checkin.objects.filter(user=request.user, active=True).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        try:
            place = Place.objects.get(pk=pk)
            zone_title = place.city.time_zone
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

        placeRepoinst = PlaceRepository()

        # MONTH
        if str(request.GET.get('period_filter')) == 'month':
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'pk': pk, 'frt': frt}
            hot_reports = PlaceRepository.getMonthReportsHot(placeRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta, 'str_pk': str_pk, 'correct_limit_from': correct_limit_from, 'correct_limit_count': correct_limit_count, 'pk': pk, 'frt': frt}
            simple_reports = PlaceRepository.getMonthReports(placeRepoinst, parameters)

        # WEEK
        elif str(request.GET.get('period_filter')) == 'week':
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'pk': pk, 'frt': frt}
            hot_reports = PlaceRepository.getWeekReportsHot(placeRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta, 'str_pk': str_pk, 'correct_limit_from': correct_limit_from, 'correct_limit_count': correct_limit_count, 'pk': pk, 'frt': frt}
            simple_reports = PlaceRepository.getWeekReports(placeRepoinst, parameters)

        # TODAY
        else:
            # Hot reports
            parameters = {'tz_delta': tz_delta, 'pk': pk, 'frt': frt}
            hot_reports = PlaceRepository.getTodayReportsHot(placeRepoinst, parameters)
            serializer_hot_reports = ReportForListSerializer(hot_reports, many=True, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks, 'request': request})

            # Remove duplicates
            hot_data = self.getHotData(serializer_hot_reports)
            str_pk = hot_data['str_pk']

            # Correction limits
            hot_count = hot_data['hot_count']
            correct_limit_from = self.correctionLimitFrom(limit_from, hot_count)
            correct_limit_count = self.correctionLimitCount(limit_from, limit_count, hot_count)

            # Simple reports
            parameters = {'tz_delta': tz_delta, 'str_pk': str_pk, 'correct_limit_from': correct_limit_from, 'correct_limit_count': correct_limit_count, 'pk': pk, 'frt': frt}
            simple_reports = PlaceRepository.getTodayReports(placeRepoinst, parameters)

        # IF limit_from > hot_count => Hot_places does not view
        if (correct_limit_from + hot_count) > hot_count:
            hot_reports_result = []
        else:
            hot_reports_result = serializer_hot_reports.data
        serializer_simple_reports = ReportForListSerializer(simple_reports, many=True, context={'my_like_report_pks': my_like_report_pks, 'request': request})

        place = self.get_object(pk)
        serializer_place = PlaceDetailSerializer(place, context={
            'my_check_in': my_check_in,
            'my_check_in_entity': my_checin,
            'my_like_place_pks': my_like_place_pks
        })

        return Response({
            'place': serializer_place.data
            , 'reports': hot_reports_result + serializer_simple_reports.data
            # , 'field_for_testing(simple_pl)': hot_reports_result
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
            limit_from = int(hot_count)
            return limit_from
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


class CheckinList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        checkin = Checkin.objects.all()
        serializer = CheckinSerializer(checkin, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))



        try:
            place = Place.objects.get(pk=request.POST.get('place_pk'))
        except Place.DoesNotExist:
            return Response({'error': 'Invalid place_pk'}, status=status.HTTP_400_BAD_REQUEST)

        # set date when was created last report
        place.created_lst_rpt = now_utc
        place.save()


        # data for Add points
        data = {
                    'user': request.user,
                    'place': place,
                }
        point_manager = PointManager()
        notify_manager = NotificationManager()

        checkin = Checkin.objects.filter(user=request.user, place=place).first()
        if checkin is None:
            d = {'user': request.user.pk, 'place': request.POST.get('place_pk'), 'is_hidden': request.POST.get('is_hidden')}
            serializer = CheckinSerializer(data=d, context={'request': request})
            if serializer.is_valid():
                self.clear_old_check_ins(request.user)
                serializer.save()

                #  Add points
                point_manager.add_point_by_type('check-in', data)

                # Send notifications
                # import ipdb;ipdb.set_trace()
                check_in = Checkin.objects.get(pk=serializer.data['pk'])
                notify_manager.send_check_in_notify(check_in)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if 'is_hidden' in request.POST:
                hidden = str(request.POST.get('is_hidden'))
                if hidden.lower() == 'true':
                    checkin.is_hidden = True
                else:
                    checkin.is_hidden = False

            #  Add points
            if now_utc > checkin.expired:
                point_manager.add_point_by_type('check-in', data)

                # Send notifications
                notify_manager.send_check_in_notify(checkin)


            manager = ReportManager()
            expired_time = manager.get_expired_time(checkin.place.city)

            checkin.expired = expired_time
            checkin.created = datetime.now()
            checkin.active = True

            # Enable old active check-ins
            self.clear_old_check_ins(request.user)

            checkin.save()
            serializer = CheckinSerializer(checkin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def clear_old_check_ins(self, user):
        checkins = Checkin.objects.filter(user=user, active=True)
        if checkins.count() > 0:
            for check in checkins:
                check.active = False
                check.save()

        return True


class LikeList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        limitFrom = str(request.GET.get('limit_from'))
        limitCount = str(request.GET.get('limit_count'))

        if limitFrom == 'None':
            limitFrom = '0'
        if limitCount == 'None':
            limitCount = '100000'

        user_id = str(request.user.id)

        places = Place.objects.raw(
            'SELECT '
                'places_place.id , '
                'places_place.city_id , '
                'places_place.title, '
                'places_place.address, '
                'places_place.description, '
                'places_place.enable, '
                'places_place.created, '
                'places_place.created_lst_rpt '

            'FROM places_like '
            'LEFT JOIN places_place  ON places_place.id = places_like.place_id '
            
            'WHERE places_like.user_id = '+user_id+' '
            'GROUP BY places_place.id '
            'ORDER BY places_place.created_lst_rpt DESC '
            'LIMIT '+limitFrom+', '+limitCount+''
        )

        my_checin = Checkin.objects.filter(user=request.user, active=True).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk

        # My likes
        my_like_place_pks = []
        my_likes = Like.objects.filter(user=request.user)
        if my_likes.count() > 0:
            for i in my_likes:
                my_like_place_pks += [str(i.place.pk)]

        serializer = PlaceSerializer(places, many=True, context={
            'my_check_in': my_check_in,
            'my_check_in_entity': my_checin,
            'my_like_place_pks': my_like_place_pks,

        })
        return Response({"places": serializer.data})

    # Create Like
    def post(self, request, format=None):
        place_id = request.POST.get('place_pk')
        user_id = request.user.id
        like = Like.objects.filter(place_id=place_id, user=request.user).first()

        # Remove Like
        if 'remove_like' in request.POST:
            if like is None:
                pass
            else:
                remove = str(request.POST.get('remove_like'))
                if remove.lower() == 'true':
                    like.delete()
                    return Response({'data': 'successfully remove.'}, status=status.HTTP_200_OK)

        # Create just one like for user in this place
        if like is None:
            # request.data.update()
            serializer = LikeSerializer(data={'user': user_id, 'place': place_id}, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'pk': str(like.pk), 'place': str(place_id), 'user': str(user_id)}, status=status.HTTP_201_CREATED)



class CityList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        latitude = str(request.GET.get('latitude'))
        longitude = str(request.GET.get('longitude'))

        if latitude == 'None':
            return Response({'error': 'Invalid or missing perameter latitude in u request'}, status=status.HTTP_400_BAD_REQUEST)
        if longitude == 'None':
            return Response({'error': 'Invalid or missing perameter longitude in u request'}, status=status.HTTP_400_BAD_REQUEST)

        cities = City.objects.raw(
                'SELECT '
                    'city_city.id, '
                    'city_city.title, '
                    'city_city.latitude, '
                    'city_city.longitude, '

                    'COUNT(places_place.id) AS cnt, '
                    'ROUND(( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( city_city.latitude ) ) * '
                    'cos( radians( city_city.longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                    '* sin( radians( city_city.latitude ) ) ) ) * 1000 / 1609.34, 1) AS distance '

                ' FROM city_city '
                ' LEFT JOIN places_place  ON places_place.city_id = city_city.id'
                ' WHERE city_city.enable = 1 '
                ' GROUP BY city_city.id '
                ' HAVING cnt > 0 '
                ' ORDER BY ROUND(( 6371 * acos( cos( radians('+latitude+') ) * cos( radians( latitude ) ) * '
                    'cos( radians( longitude ) - radians('+longitude+') ) + sin( radians('+latitude+') ) '
                    '* sin( radians( latitude ) ) ) ) * 1000 / 1609.34, 1) '
                    '  ASC '

            )
        city_serializer = CitySerializer(cities, many=True)

        return Response({'cities': city_serializer.data})


class PlaceToDancer(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Create Like
    def post(self, request, format=None):
        place_id = request.POST.get('place_pk')
        try:
            place = Place.objects.get(id=place_id)
        except:
            raise Http404
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return Response({'data': 'Only dancer can update place'}, status=status.HTTP_400_BAD_REQUEST)

        if profile.type != 1:
            return Response({'data': 'Only dancer can update place'}, status=status.HTTP_400_BAD_REQUEST)

        profile.place = place
        profile.save()

        return Response({'data': 'successfully updated'}, status=status.HTTP_201_CREATED)