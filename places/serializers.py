from rest_framework import serializers
from places.models import Place, Checkin, Like
from django.conf import settings
from django.db.models.functions import Lower
from apiusers.serializers import LastUsersSerializer


class PlaceDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=100)
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)
    opening_hours = serializers.CharField(required=True, allow_blank=True, max_length=100)
    music_type = serializers.CharField(required=True, allow_blank=True, max_length=100)
    age_group = serializers.CharField(required=True, allow_blank=True, max_length=100)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    place_image = serializers.SerializerMethodField()
    place_logo = serializers.SerializerMethodField()
    checkin_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    last_users = serializers.SerializerMethodField()
    my_check_in = serializers.SerializerMethodField()

    def get_checkin_cnt(self, obj):
        return obj.checkin_set.count()

    def get_like_cnt(self, obj):
        return obj.like_set.count()

    def get_place_image(self, obj):

        if str(obj.image) != '':
            puth = str(obj.image)
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None

        return res

    def get_place_logo(self, obj):

        if str(obj.logo) != '':
            puth = str(obj.logo)
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None

        return res

    def get_last_users(self, obj):
        last_checkins = Checkin.objects.filter(is_hidden=False, place=obj).order_by(Lower('created').desc())[0:10]
        serializer = LastUsersSerializer(last_checkins, many=True)
        return serializer.data

    def get_my_check_in(self, obj):

        try:
            my_check_in = self.context['my_check_in']
        except:
            my_check_in = None

        if obj.pk == my_check_in:
            res = True
        else:
            res = False
        return res

class PlaceSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=100)
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    enable = serializers.BooleanField(required=False)
    created = serializers.DateTimeField()
    created_lst_rpt = serializers.DateTimeField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    place_image = serializers.SerializerMethodField()
    place_logo = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    checkin_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    last_users = serializers.SerializerMethodField()
    my_check_in = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()


    def get_all_city(self, obj):
        return None


    def get_city(self, obj):

        if obj.city is not None:
            city = obj.city.title
        else:
            city = None
        return city


    def get_my_check_in(self, obj):

        try:
            my_check_in = self.context['my_check_in']
        except:
            my_check_in = None

        if obj.pk == my_check_in:
            res = True
        else:
            res = False
        return res

    def get_place_image(self, obj):

        if str(obj.image) != '':
            puth = str(obj.image)
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None

        return res

    def get_place_logo(self, obj):

        if str(obj.logo) != '':
            puth = str(obj.logo)
            res = settings.SITE_DOMAIN
            res += '/media/'
            res += puth
        else:
            res = None

        return res

    def get_last_users(self, obj):
        last_checkins = Checkin.objects.filter(is_hidden=False, place=obj).order_by(Lower('created').desc())[0:10]
        serializer = LastUsersSerializer(last_checkins, many=True)
        return serializer.data

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Place.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.enable = validated_data.get('enable', instance.enable)

        instance.save()
        return instance

    def get_distance(self, obj):
        try:
            distance = obj.distance
        except AttributeError:
            distance = 0
        return distance

    def get_checkin_cnt(self, obj):
        try:
            checkin_cnt = obj.checkin_cnt
        except AttributeError:
            checkin_cnt = 0
        return checkin_cnt

    def get_like_cnt(self, obj):
        try:
            like_cnt = obj.like_cnt
        except AttributeError:
            like_cnt = 0
        return like_cnt


class CheckinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkin
        fields = ('pk', 'user', 'place')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('pk', 'place', 'user',)

    # def save(self, **kwargs):
    #     like = super(LikeSerializer, self).save(**kwargs)
    #     like.user = self.context['request'].user
    #     try:
    #         place = Place.objects.get(pk=self.context['request'].POST.get('place_pk'))
    #         like.place = place
    #     except Place.DoesNotExist:
    #         raise Http404
    #
        # return like.save()

