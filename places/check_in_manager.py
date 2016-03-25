import pytz


class CheckInManager():

    def __init__(self):
        self.x = None

    # EXPIRED CHECK IN TIME
    def get_expired_time(self, check_in):
        from pytz import timezone
        from datetime import datetime, timedelta

        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))

        # Convert to US/Pacific time zone
        zone_name = check_in.place.city.time_zone
        now_with_zone = now_utc.astimezone(timezone(zone_name))
        if now_with_zone.hour > 6:

            # set next day 6:00
            now_with_zone += timedelta(days=1)
            now_with_zone = now_with_zone.replace(hour=6, minute=00)
        else:
            # set today 6:00
            now_with_zone = now_with_zone.replace(hour=6, minute=00)

        expired_utc = now_with_zone.astimezone(pytz.utc)

        return expired_utc