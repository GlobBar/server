from django.forms.models import fields_for_model
from rest_framework import serializers
from places.models import Place, Checkin, Like
from django.http import Http404

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
    distance = serializers.SerializerMethodField()
    checkin_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()

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
        # import ipdb; ipdb.set_trace()
        try:
            distance = obj.distance
        except AttributeError:
            distance = 0
        return distance

    def get_checkin_cnt(self, obj):
        # import ipdb; ipdb.set_trace()
        try:
            checkin_cnt = obj.checkin_cnt
        except AttributeError:
            checkin_cnt = 0
        return checkin_cnt

    def get_like_cnt(self, obj):
        # import ipdb; ipdb.set_trace()
        try:
            like_cnt = obj.like_cnt
        except AttributeError:
            like_cnt = 0
        return like_cnt


class CheckinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkin
        fields = ('pk', 'user', )

    def save(self, **kwargs):

        checkin = Checkin.objects.filter(user=self.context['request'].user).first()
        if checkin is not None:
            checkin.delete()

        checkin = super(CheckinSerializer, self).save(**kwargs)
        checkin.user = self.context['request'].user

        try:
            place = Place.objects.get(pk=self.context['request'].POST.get('place_pk'))
            checkin.place = place
        except Place.DoesNotExist:
            raise Http404
        checkin.save()
        return checkin


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('pk', 'place', 'user',)

    def save(self, **kwargs):
        like = super(LikeSerializer, self).save(**kwargs)
        like.user = self.context['request'].user
        try:
            place = Place.objects.get(pk=self.context['request'].POST.get('place_pk'))
            like.place = place
        except Place.DoesNotExist:
            raise Http404

        return like.save()

