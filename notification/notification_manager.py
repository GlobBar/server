from notification_sender import IosSender, AndroidSender


class NotificationManager:

    def __init__(self): pass

    @staticmethod
    def get_notification_strategy(device):
        if device.type == 1:
            notification_strategy = AndroidSender()
        elif device.type == 2:
            notification_strategy = IosSender()
        else:
            notification_strategy = None

        return notification_strategy


