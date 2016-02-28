from places.models import Place, Checkin, Like
from places.serializers import PlaceSerializer, CheckinSerializer, LikeSerializer, PlaceDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from city.models import City
from city.serializers import CitySerializer
from django.db import connection
from report.serializers import ReportSerializer


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
        my_checin = Checkin.objects.filter(user=request.user).first()
        if my_checin is None:
            my_check_in = None
        else:
            my_check_in = my_checin.place.pk
        # import ipdb;ipdb.set_trace()

        hot_reports = Place.objects.raw(
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
                'ri.image AS image_from_query, '
                'COUNT(l.id) as like_cnt '
            'FROM report_report '
            'LEFT JOIN report_reportimagelike l ON l.report_id = report_report.id '
            'LEFT JOIN files_reportimage ri ON ri.id = report_report.report_image_id '
            'WHERE report_report.place_id = '+pk+' AND report_report.enable = 1 '
            'GROUP BY report_report.id '
            'ORDER BY like_cnt DESC '
            'LIMIT 0,3'
        )
        # import ipdb;ipdb.set_trace()
        serializer_hgot_reports = ReportSerializer(hot_reports, many=True)

        place = self.get_object(pk)
        serializer_place = PlaceDetailSerializer(place, context={'my_check_in': my_check_in})
        return Response({'place': serializer_place.data, 'reports': serializer_hgot_reports.data})

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


class CheckinList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        checkin = Checkin.objects.all()
        serializer = CheckinSerializer(checkin, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        checkin = Checkin.objects.filter(user=request.user).first()

        if checkin is None:
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
            serializer = LikeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'pk': str(like.pk), 'place': str(place_id), 'user': str(user_id)}, status=status.HTTP_201_CREATED)



