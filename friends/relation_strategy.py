from friends.models import Relation


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
        return self.create_relation_base(user, friend, status, revers_status)


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
