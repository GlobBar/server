from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import connection
from notification.notification_manager import NotificationManager
from django.conf import settings


# For single messages from User to User
class Messages(models.Model):
    user_to = models.IntegerField(null=True, blank=True)
    user_from = models.ForeignKey(User,  null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, default='')
    body = models.TextField(blank=False,)
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    is_readed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


# For admin messages to All Users (for example news)
class NewsMessages(models.Model):
    user_from = models.ForeignKey(User,  null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, default='')
    body = models.TextField(blank=False,)
    status = models.IntegerField(null=True, blank=True)
    is_pushed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = "News"
        verbose_name_plural = "News"


# For single messages from User to User
class EmailMessage(models.Model):
    user_to = models.ForeignKey(User, null=True, blank=True, help_text="Choose an user id, or empty to send all")
    subject  = models.CharField(max_length=255, blank=False, default='')
    text = models.TextField(blank=False, )
    is_sent = models.IntegerField(null=True, blank=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = "Email"
        verbose_name_plural = "Emails"

# method for updating
@receiver(post_save, sender=NewsMessages, dispatch_uid="create_all_users_message")
def update_stock(sender, instance, **kwargs):


    # Current time in UTC
    from pytz import timezone
    from datetime import datetime
    now_utc = datetime.now(timezone('UTC'))

    users = User.objects.filter(is_active=True)
    newLanguages = []

    for usr in users:
        newLanguages += [(instance.title, instance.body, usr.pk, now_utc)]


    cursor = connection.cursor()
    cursor.executemany("insert into `user_messages_messages` (title, body, user_to, created) values (%s, %s, %s, %s)", newLanguages)

    # Send notifications
    push_users = users[:2000] #ToDo cron tasks
    notify_manager = NotificationManager()
    notify_manager.send_news_notify(push_users)


# method for send emails to all
@receiver(post_save, sender=EmailMessage, dispatch_uid="create_all_users_emails")
def update_emails(sender, instance, **kwargs):

    import sendgrid
    from django.template import loader

    if instance.user_to is None:
        users = User.objects.filter(is_active=True)[:2000] #ToDo cron tasks
    else:
        users = User.objects.filter(is_active=True, pk=instance.user_to.pk)

    # APIkey
    sg = sendgrid.SendGridClient(settings.SEND_GRID_API_KEY)
    context = {
        'userName': 'testUser',
        'text': instance.text,
        'subject': instance.subject
    }

    body_html = loader.get_template('notification/emails/simple_email.html').render(context)


    for usr in users:
        if usr.email is not None and len(usr.email) > 10:
            message = sendgrid.Mail(
                to=usr.email,
                subject=instance.subject,
                html=body_html,
                text='Body',
                from_email='newsletter@partyzhere.com')
            status, msg = sg.send(message)

