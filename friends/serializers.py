from rest_framework import serializers
from friends.models import Relation, Following, Follower
from django.conf import settings
import os


# class RelationSerializer(serializers.ModelSerializer):
#
#     user = serializers.SerializerMethodField()
#
#     def get_user(self, obj):
#         # import ipdb;ipdb.set_trace()
#         return {
#             'pk': obj.user_pk,
#             'username': obj.user_name,
#             'profile_image': self.get_image_link(RelationSerializer, obj)
#         }
#
#     @staticmethod
#     def get_image_link(self, obj):
#         try:
#             puth = str(obj.user_image)
#             if puth == 'None':
#                 anonim = settings.MEDIA_ROOT
#                 anonim += '/anonim.jpg'
#                 if os.path.isfile(anonim):
#                     my_file = settings.SITE_DOMAIN
#                     my_file += '/media/anonim.jpg'
#                 else:
#                     my_file = None
#
#             else:
#                 is_absolut_puth = puth.find('http')
#
#                 if is_absolut_puth == -1:
#                     my_file = settings.SITE_DOMAIN
#                     my_file += '/media/'
#                     my_file += puth
#                 else:
#                     my_file = puth
#         except:
#             anonim = settings.MEDIA_ROOT
#             anonim += '/anonim.jpg'
#             if os.path.isfile(anonim):
#                 my_file = settings.SITE_DOMAIN
#                 my_file += '/media/anonim.jpg'
#             else:
#                 my_file = None
#
#         return my_file
#
#     class Meta:
#         model = Relation
#         fields = ('pk', 'user', 'status')

class RelationSerializer(serializers.ModelSerializer):

    pk = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    def get_pk(self, obj):
        return obj.user_pk

    def get_username(self, obj):
        return obj.user_name

    def get_profile_image(self, obj):
        return self.get_image_link(RelationSerializer, obj)

    @staticmethod
    def get_image_link(self, obj):
        try:
            puth = str(obj.user_image)
            if puth == 'None':
                anonim = settings.MEDIA_ROOT
                anonim += '/anonim.jpg'
                if os.path.isfile(anonim):
                    my_file = settings.SITE_DOMAIN
                    my_file += '/media/anonim.jpg'
                else:
                    my_file = None

            else:
                is_absolut_puth = puth.find('http')

                if is_absolut_puth == -1:
                    my_file = settings.SITE_DOMAIN
                    my_file += '/media/'
                    my_file += puth
                else:
                    my_file = puth
        except:
            anonim = settings.MEDIA_ROOT
            anonim += '/anonim.jpg'
            if os.path.isfile(anonim):
                my_file = settings.SITE_DOMAIN
                my_file += '/media/anonim.jpg'
            else:
                my_file = None

        return my_file

    class Meta:
        model = Relation
        fields = ('pk', 'username', 'profile_image')


class FollowerSerializer(serializers.ModelSerializer):

    pk = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    def get_pk(self, obj):
        return obj.user_pk

    def get_username(self, obj):
        return obj.user_name

    def get_profile_image(self, obj):
        return self.get_image_link(RelationSerializer, obj)

    @staticmethod
    def get_image_link(self, obj):
        try:
            puth = str(obj.user_image)
            # import ipdb;ipdb.set_trace()
            if puth == 'None' or puth == '':
                anonim = settings.MEDIA_ROOT
                anonim += '/anonim.jpg'
                if os.path.isfile(anonim):
                    my_file = settings.SITE_DOMAIN
                    my_file += '/media/anonim.jpg'
                else:
                    my_file = None

            else:
                is_absolut_puth = puth.find('http')

                if is_absolut_puth == -1:
                    my_file = settings.SITE_DOMAIN
                    my_file += '/media/'
                    my_file += puth
                else:
                    my_file = puth
        except:
            anonim = settings.MEDIA_ROOT
            anonim += '/anonim.jpg'
            if os.path.isfile(anonim):
                my_file = settings.SITE_DOMAIN
                my_file += '/media/anonim.jpg'
            else:
                my_file = None

        return my_file

    class Meta:
        model = Follower
        fields = ('pk', 'username', 'profile_image')



