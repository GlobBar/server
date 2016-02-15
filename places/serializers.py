from rest_framework import serializers
from places.models import Place


class PlaceSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=100)
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    enable = serializers.BooleanField(required=False)
    created = serializers.DateTimeField()


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
