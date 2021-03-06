from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from apiusers.serializers import UserDetailSerializer
from apiusers.balance_manager import BalanceManager
from points.models import PointsCount, Transactions, FeeSize
from report.models import Report, UsersWithUnlockedMedia
from points.serializers import PointSerializer
from pytz import timezone
from datetime import datetime
from rest_framework import status
from django.http import Http404
from user_messages.models import Messages
from notification.notification_manager import NotificationManager


class PointsList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        point_serializer = PointSerializer(point_count)

        return Response(point_serializer.data)

    def post(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, user=request.user)
            point_count.save()

        # Update points
        exist_points = point_count.points
        spent_points_data = request.POST.get('spent_points')
        if spent_points_data == 'None':
            spent_points = 0
        else:
            spent_points = int(spent_points_data)

        if spent_points > exist_points:
            return Response({'error': ('You try to spent more points then you have !')}, status=status.HTTP_400_BAD_REQUEST)

        now_utc = datetime.now(timezone('UTC'))
        updated_points = exist_points - spent_points
        point_count.points = updated_points
        point_count.updated = now_utc
        point_count.save()

        point_serializer = PointSerializer(point_count)

        return Response(point_serializer.data)

class BalanceUp(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            point_count = PointsCount.objects.get(user=request.user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=request.user)
            point_count.save()

        # Update balance
        exist_balance = point_count.balance
        if exist_balance is None:
            exist_balance = 0
        balance_delta = request.POST.get('balance_delta')

        now_utc = datetime.now(timezone('UTC'))
        updated_balance = exist_balance + int(balance_delta)
        point_count.points = 0
        point_count.balance = updated_balance
        point_count.updated = now_utc
        point_count.save()

        user_serializer = UserDetailSerializer(request.user)

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)


class BalanceDonate(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        current_user = request.user

        try:
            user = User.objects.get(pk=request.POST.get('pk'))
        except User.DoesNotExist:
            raise Http404

        if current_user.id == user.id:
            return Response({'error': ('You try to donate your self !')}, status=status.HTTP_400_BAD_REQUEST)

        balance_delta = int(request.POST.get('amount'))

        current_user_point_count = self.poin_count_by_user(current_user)
        point_count = self.poin_count_by_user(user)
        if balance_delta > current_user_point_count.balance:
            return Response({'error': ('You try to spent more maney then you have !')}, status=status.HTTP_400_BAD_REQUEST)
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
        body = current_user.username+' donated you '+str(float(balance_delta)/100)+'$'
        message = Messages(title='Balance update', body=body, user_from=current_user, user_to=user.id, created=now_utc, is_readed=0)
        message.save()

        # Send notifications
        notify_manager = NotificationManager()
        # notify_manager.send_donate_notify(user, body)

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)

    def poin_count_by_user(self, user):
        try:
            point_count = PointsCount.objects.get(user=user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=user)
            point_count.save()

        return point_count

class BalanceMediaDonate(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        current_user = request.user
        balance_manager = BalanceManager()

        try:
            report = Report.objects.get(pk=request.POST.get('report_pk'))
            user = report.user
        except Report.DoesNotExist:
            raise Http404

        if current_user.id == user.id:
            return Response({'error': ('You try to donate your self !')}, status=status.HTTP_400_BAD_REQUEST)


        if report.is_locked == False:
            return Response({'error': ('You try to donate free media item !')}, status=status.HTTP_400_BAD_REQUEST)

        balance_delta = int(request.POST.get('amount'))
        current_user_point_count = balance_manager.poin_count_by_user(current_user)
        point_count = balance_manager.poin_count_by_user(user)
        if balance_delta > current_user_point_count.balance:
            return Response({'error': ('You try to spent more maney then you have !')},
                            status=status.HTTP_400_BAD_REQUEST)
        balance_manager.donate(point_count, balance_delta, current_user_point_count, current_user, user)

        try:
            UsersWithUnlockedMedia.objects.get(user=request.user, report=report)
        except UsersWithUnlockedMedia.DoesNotExist:
            users_with_unlocked_media = UsersWithUnlockedMedia(user=request.user, report=report, created=datetime.now(timezone('UTC')))
            users_with_unlocked_media.save()

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)


class CashOut(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def poin_count_by_user(self, user):
        try:
            point_count = PointsCount.objects.get(user=user)
            if point_count.balance is None:
                point_count.balance = 0
        except PointsCount.DoesNotExist:
            point_count = PointsCount(points=0, balance=0, user=user)
            point_count.save()

        return point_count

    def post(self, request, format=None):
        user = request.user
        amount = int(request.POST.get('amount'))
        finance_email = request.POST.get('email')
        if 'amount' not in request.POST.keys() or 'email' not in request.POST.keys():
            return Response({'error': ('Cant find required parameters (amount, email) !')}, status=status.HTTP_400_BAD_REQUEST)

        user_point_count = self.poin_count_by_user(user)
        if amount > user_point_count.balance:
            return Response({'error': ('You try to cash out more maney then you have !')}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transactions(finance_email=finance_email, amount=int(amount), user=user)
        transaction.save()

        user_point_count.balance = user_point_count.balance - amount
        user_point_count.save()

        return Response({"data": "Users balance has been successfully updated."}, status=status.HTTP_200_OK)

