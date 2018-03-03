from notification_sender import IosSender, AndroidSender
from places.models import Like
from pushy.models import Device
from report.report_repository import ReportRepository
from report.report_manager import ReportManager
from pytz import timezone
from datetime import datetime
from friends.models import Relation, Follower
from notification.models import PushNotifications


class NotificationManager:

    def __init__(self): pass

    @staticmethod
    def get_notification_strategy(device):
        if device.type == 1:
            notification_strategy = AndroidSender.get_instance(AndroidSender())
        elif device.type == 2:
            notification_strategy = IosSender.get_instance(IosSender())
        else:
            notification_strategy = None

        return notification_strategy

    # Your saved venue is HOT
    def send_hot_plases_notify(self, report):
        place = report.place
        report_repository = ReportRepository()
        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))

        # If push have not sent today yet
        if now_utc > place.last_push_expired:
            today_reports_cnt = report_repository.get_today_reports_cnt(place)
            # import ipdb; ipdb.set_trace()

            cnt = 10
            try:
                notify = PushNotifications.objects.get(name='hot_venue')
                cnt = notify.count
            except PushNotifications.DoesNotExist:
                pass

            # If place is HOT
            if today_reports_cnt > cnt:
                likes = Like.objects.filter(place=place)[0:100]  # TODO create Cron task to send notifications queue
                notification_manager = NotificationManager()

                for lk in likes:
                    try:
                        device = Device.objects.get(user=lk.user)
                        # Get notification strategy
                        notification_sender = notification_manager.get_notification_strategy(device)
                        # Send message
                        notification_sender.set_device_token(device.key).set_title('Your saved venue '+place.title+' is hot tonight.').set_data({'type': 3, 'club_id': place.pk}).send_message()

                    except Device.DoesNotExist:
                        pass
        report_manager = ReportManager()

        # Set expired date , before this date system can't send push notification about your saved place is hot tonight
        # So user get this kind of notify just one's a day
        place.last_push_expired = report_manager.get_expired_time(place.city)
        place.save()
        return True

    # CHECK-IN notifications
    def send_check_in_notify(self, check_in):
        user = check_in.user
        place = check_in.place
        notification_manager = NotificationManager()

        if check_in.is_hidden is False:
            # Followers

            followers = Follower.objects.filter(user=check_in.user.pk)
            # import ipdb; ipdb.set_trace()
            for follower in followers:
                try:
                    device = Device.objects.get(user=follower.friend)
                    # Get notification strategy
                    notification_sender = notification_manager.get_notification_strategy(device)
                    # Send message
                    notification_sender.set_device_token(device.key).set_title(user.username+' just checked in at '+place.title+'.').set_data({'type': 2, 'club_id': place.pk, 'user_id': user.pk}).send_message()

                except Device.DoesNotExist:
                    pass
        return True

    # NEWS notifications
    def send_news_notify(self, users):
        notification_manager = NotificationManager()

        for user in users:
            try:
                device = Device.objects.get(user=user)
                # Get notification strategy
                notification_sender = notification_manager.get_notification_strategy(device)
                # Send message
                notification_sender.set_device_token(device.key).set_title('We have venue news!').set_data({'type': 4}).send_message()
            except Device.DoesNotExist:
                pass

        return True

    # Donate notifications
    def send_donate_notify(self, user, message):
        notification_manager = NotificationManager()

        try:
            device = Device.objects.get(user=user)
            # Get notification strategy
            notification_sender = notification_manager.get_notification_strategy(device)
            # Send message
            notification_sender.set_device_token(device.key).set_title(message).set_data(
                {'type': 6}).send_message()
        except Device.DoesNotExist:
            pass

        return True

    # Transaction notifications
    def send_transaction_notify(self, user, message):
        notification_manager = NotificationManager()

        try:
            device = Device.objects.get(user=user)
            # Get notification strategy
            notification_sender = notification_manager.get_notification_strategy(device)
            # Send message
            notification_sender.set_device_token(device.key).set_title(message).set_data(
                {'type': 6}).send_message()
        except Device.DoesNotExist:
            pass

        return True
