import pytz
from pytz import timezone
from datetime import datetime, timedelta
from points.models import PointsCount, Transactions, FeeSize
from report.models import Report
from points.serializers import PointSerializer
from pytz import timezone
from datetime import datetime
from rest_framework import status
from django.http import Http404
from user_messages.models import Messages
from notification.notification_manager import NotificationManager

class BalanceManager():

    def __init__(self):
        pass

    def donate(self, point_count, balance_delta, current_user_point_count, current_user, user):

        fee_size = 1 - (FeeSize.objects.all()[0].fee / 100)
        balance_delta_minus_fee = balance_delta * fee_size
        # Update balance
        now_utc = datetime.now(timezone('UTC'))
        point_count.balance = point_count.balance + balance_delta_minus_fee
        point_count.updated = now_utc
        point_count.save()

        current_user_point_count.balance = current_user_point_count.balance - balance_delta
        current_user_point_count.updated = now_utc
        current_user_point_count.save()

        # Creating Message
        body = current_user.username + ' donated you ' + str(float(balance_delta) / 100) + '$'
        message = Messages(title='Balance update', body=body, user_from=current_user, user_to=user.id, created=now_utc,
                           is_readed=0)
        message.save()

        # Send notifications
        # notify_manager = NotificationManager()
        # notify_manager.send_donate_notify(user, body)

        return None

    def poin_count_by_user(self, user):
        try:
            point_count = PointsCount.objects.get(user=user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=user)
            point_count.save()

        return point_count