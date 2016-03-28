from pytz import timezone
from datetime import datetime
from points.models import PointType, PointsCount


class PointManager():

    def __init__(self):
        pass

    def add_point_by_type(self, type, data):
        try:
            point_type = PointType.objects.get(name=type)
        except PointType.DoesNotExist:
            return None

        # Exist Points
        exist_points_obj = self.get_current_points(data['user'])
        exist_points = exist_points_obj.points

        # New points
        place = data['place']
        if place.is_partner is True:
            new_points = point_type.points_count_partner
        else:
            new_points = point_type.points_count

        # Update points
        now_utc = datetime.now(timezone('UTC'))
        updated_points = exist_points + new_points
        exist_points_obj.points = updated_points
        exist_points_obj.updated = now_utc
        exist_points_obj.save()

        return True

    # Return Current user PointsCount obj or create new one
    def get_current_points(self, user):
        try:
            points = PointsCount.objects.get(user=user)
        except PointsCount.DoesNotExist:
            points = PointsCount(points=0, user=user)
            points.save()
        return points


