import pytz
from pytz import timezone
from datetime import datetime, timedelta

class ReportManager():

    def __init__(self):
        pass

    #  REPORT EXPIRED TIME
    def get_expired_time(self, city):

        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))

        # Convert to US/Pacific time zone
        try:
            zone_name = city.time_zone
            now_with_zone = now_utc.astimezone(timezone(zone_name))

        except AttributeError:
            now_with_zone = now_utc.astimezone(timezone('UTC'))

        if now_with_zone.hour >= 6:

            # set next day 6:00
            now_with_zone += timedelta(days=1)
            now_with_zone = now_with_zone.replace(hour=6, minute=00)
        else:
            # set today 6:00
            now_with_zone = now_with_zone.replace(hour=6, minute=00)

        expired_utc = now_with_zone.astimezone(pytz.utc)

        return expired_utc
