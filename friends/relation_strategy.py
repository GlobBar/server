from friends.models import Relation
from pushy.models import Device
from notification.notification_manager import NotificationManager


class RelationAbstract:
    """ Inteface / Abstract Class concept for relation. """
    FRIEND_STATUS = 1
    SEND_REQUEST_STATUS = 2
    GET_REQUEST_STATUS = 3
    FOLLOWER_STATUS = 4  # Friend following his user
    FOLLOWING_STATUS = 5  # User following his friend

    def __init__(self):
        pass

    def create_relation_base(self, user, friend, status, revers_status):
        self.remove_relation(user, friend)
        new_relation = Relation(user=user.pk, friend_id=friend.pk, status=status)
        new_relation.save()
        new_revers_relation = Relation(user=friend.pk, friend_id=user.pk, status=revers_status)
        new_revers_relation.save()

        return True

    def remove_relation(self, user, friend):
        try:
            current_relation = Relation.objects.get(user=user.pk, friend_id=friend.pk)
            current_relation.delete()
            current_relation_revers = Relation.objects.get(user=friend.pk, friend_id=user.pk)
            current_relation_revers.delete()
            return True
        except:
            pass

        return False


class RequestRelation(RelationAbstract):

    def create_relation(self, user, friend):
        status = self.SEND_REQUEST_STATUS
        revers_status = self.GET_REQUEST_STATUS
        res = self.create_relation_base(user, friend, status, revers_status)

        # Check requests count. If count >= 5 send push notify
        try:
            device = Device.objects.get(user=user)
        except Device.DoesNotExist:
            return res
        requsts = self.check_requsts(user)
        if requsts.count() > 0:
            # Get notification strategy
            notification_sender = NotificationManager().get_notification_strategy(device)
            # Send message
            notification_sender.set_device_token(device.key).set_title('New Requests').set_data({'type': 1}).send_message()

            # Sign relations as pushed
            for rel in requsts:
                rel.is_pushed = True
                rel.save()

        return res

    def check_requsts(self, user):
        MY_REQUESTS_STATUS = 3

        requests = Relation.objects.filter(status=MY_REQUESTS_STATUS, friend_id=user.pk, is_pushed=False)
        return requests


class FollowingRelation(RelationAbstract):

    def create_relation(self, user, friend):
        status = self.FOLLOWING_STATUS
        revers_status = self.FOLLOWER_STATUS
        return self.create_relation_base(user, friend, status, revers_status)


class FriendRelation(RelationAbstract):

    def create_relation(self, user, friend):
        status = self.FRIEND_STATUS
        revers_status = status
        return self.create_relation_base(user, friend, status, revers_status)
