from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import connection


# For single messages from User to User
class Messages(models.Model):
    user_to = models.IntegerField(null=True, blank=True)
    user_from = models.ForeignKey(User,  null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, default='')
    body = models.TextField(blank=False,)
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


# For admin messages to All Users (for example news)
class NewsMessages(models.Model):
    user_from = models.ForeignKey(User,  null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, default='')
    body = models.TextField(blank=False,)
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


# method for updating
@receiver(post_save, sender=NewsMessages, dispatch_uid="create_all_users_message")
def update_stock(sender, instance, **kwargs):

    users = User.objects.filter(is_active=True)
    newLanguages = []

    for usr in users:
        newLanguages += [(instance.title, instance.body, usr.pk, )]

    # push_users = users[-50:]
    # for push_u in push_users:


    # import ipdb;ipdb.set_trace()

    cursor = connection.cursor()
    cursor.executemany("insert into `user_messages_messages` (title, body, user_to) values (%s, %s, %s)", newLanguages)



