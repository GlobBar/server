import pytz
from pytz import timezone
from datetime import datetime, timedelta

class ReportManager():

    def __init__(self):
        pass

    #  REPORT EXPIRED TIME
    def get_expired_time(self, report):

        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))

        # Convert to US/Pacific time zone
        zone_name = report.place.city.time_zone
        now_with_zone = now_utc.astimezone(timezone(zone_name))
        if now_with_zone.hour >= 6:

            # set next day 6:00
            now_with_zone += timedelta(days=1)
            now_with_zone = now_with_zone.replace(hour=6, minute=00)
        else:
            # set today 6:00
            now_with_zone = now_with_zone.replace(hour=6, minute=00)

        expired_utc = now_with_zone.astimezone(pytz.utc)

        return expired_utc

    #  PLACE LAST PUSH EXPIRED TIME
    def get_place_last_push_expired(self, place):

        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))

        # Convert to US/Pacific time zone
        zone_name = place.city.time_zone
        now_with_zone = now_utc.astimezone(timezone(zone_name))
        if now_with_zone.hour >= 6:

            # set next day 6:00
            now_with_zone += timedelta(days=1)
            now_with_zone = now_with_zone.replace(hour=6, minute=00)
        else:
            # set today 6:00
            now_with_zone = now_with_zone.replace(hour=6, minute=00)

        expired_utc = now_with_zone.astimezone(pytz.utc)

        return expired_utc