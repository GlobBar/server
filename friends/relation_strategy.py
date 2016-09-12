from friends.models import Relation
from pushy.models import Device
from notification.notification_manager import NotificationManager
from friends.models import Request, Follower, Following
from notification.models import PushNotifications

class RelationAbstract:
    """ Inteface / Abstract Class concept for relation. """
    FRIEND_STATUS = 1
    SEND_REQUEST_STATUS = 2
    GET_REQUEST_STATUS = 3
    FOLLOWER_STATUS = 4  # Friend following his user
    FOLLOWING_STATUS = 5  # User following his friend

    def __init__(self):
        pass

    def create_relation_base(self, user, friend, entity):
        try:
            new_relation = entity.objects.get(user=user.pk, friend_id=friend.pk)
        except entity.DoesNotExist:
            new_relation = entity(user=user.pk, friend_id=friend.pk)
            new_relation.save()
        return new_relation

    def remove_relation_base(self, user, friend, entity):
        current_relations = entity.objects.filter(user=user.pk, friend_id=friend.pk)
        if current_relations.count() > 0:
            for c_r in current_relations:
                c_r.delete()

        return True


class RequestRelation(RelationAbstract):

    def create_relation(self, user, friend):
        cnt = 1

        # res = self.create_relation_base(user, friend, status, revers_status)
        res = self.create_relation_base(friend, user,  Request)

        # Check requests count. If count >= 5 send push notify
        try:
            device = Device.objects.get(user=friend)
        except Device.DoesNotExist:
            return res

        requsts = self.check_requsts(friend, user)

        try:
            notify = PushNotifications.objects.get(name='request')
            cnt = notify.count
        except PushNotifications.DoesNotExist:
            pass

        # import ipdb; ipdb.set_trace()
        if requsts.count() >= int(cnt):
            # Get notification strategy
            notification_sender = NotificationManager().get_notification_strategy(device)
            # Send message
            notification_sender.set_device_token(device.key).set_title('You have '+str(requsts.count())+' new following requests. Manage the requests?').set_data({'type': 1}).send_message()

            # Sign relations as pushed
            for rel in requsts:
                rel.is_pushed = True
                rel.save()

        return res

    def check_requsts(self, user, friend):
        requests = Request.objects.filter(user=user.pk, is_pushed=False)
        return requests

    def remove_relation(self, user, friend):
        res = self.remove_relation_base(user, friend, Request)
        return res


class FollowingRelation(RelationAbstract):

    def create_relation(self, user, friend):

        self.remove_relation_base(user, friend, Request)

        self.create_relation_base(user, friend, Follower)
        self.create_relation_base(friend, user, Following)

        return

    def remove_relation(self, user, friend):

        self.remove_relation_base(user, friend, Following)
        self.remove_relation_base(friend, user, Follower)

        return True


class FollowerRelation(RelationAbstract):

    def create_relation(self, user, friend):

        self.remove_relation_base(user, friend, Request)

        self.create_relation_base(user, friend, Following)
        self.create_relation_base(friend, user, Follower)

        return

    def remove_relation(self, user, friend):

        self.remove_relation_base(user, friend, Follower)
        self.remove_relation_base(friend, user, Following)

        return True

class FriendRelation(RelationAbstract):

    def create_relation(self, user, friend):
        status = self.FRIEND_STATUS
        revers_status = status
        return self.create_relation_base(user, friend, status, revers_status)
