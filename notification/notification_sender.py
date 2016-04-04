from abc import ABCMeta, abstractmethod
from django.conf import settings


class AbstractSender:
    __metaclass__ = ABCMeta

    def __init__(self): pass

    @abstractmethod
    def set_title(self, data): pass

    @abstractmethod
    def set_data(self, data): pass

    @abstractmethod
    def send_message(self): pass

    @abstractmethod
    def set_device_token(self, token): pass




# iOS
class IosSender(AbstractSender):
    notify_data = {'foo': 'bar'}
    device_token = ''
    notify_title = 'New notification'
    instance = None

    def get_instance(self):
        if self.instance is None:
            return IosSender()
        else:
            return self.instance

    def set_title(self, title):
        self.notify_title = title
        return self

    def set_data(self, data):
        self.notify_data = data
        return self

    def set_device_token(self, token):
        self.device_token = token
        return self

    def send_message(self):

        import socket, ssl, json, struct
        import binascii

        deviceToken = str(self.device_token)

        thePayLoad = {
             'aps': {
                  'alert': self.notify_title,
                  'sound': 'default',
                  'badge': 42
                  },
             'data': self.notify_data,
             }

        theCertfile = settings.PEM_KEY_DIR
        theHost = ('gateway.sandbox.push.apple.com', 2195)
        data = json.dumps(thePayLoad)
        deviceToken = deviceToken.replace(' ','')
        byteToken = binascii.unhexlify(deviceToken)
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack(theFormat, 0, 32, byteToken, len(data), data)
        ssl_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=theCertfile)
        ssl_sock.connect(theHost)
        ssl_sock.write(theNotification)
        ssl_sock.close()

        return True


# Android
class AndroidSender(AbstractSender):
    notify_data = {'foo': 'bar'}
    device_token = ''
    notify_title = 'New notification'
    instance = None

    def get_instance(self):
        if self.instance is None:
            return IosSender()
        else:
            return self.instance

    def set_title(self, title):
        self.notify_title = title
        return True

    def set_data(self, data):
        self.notify_data = data
        return True

    def set_device_token(self, token):
        self.device_token = token
        return True

    def send_message(self):
        return None

