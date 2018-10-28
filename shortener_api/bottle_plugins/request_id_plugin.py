import threading
import time

import bottle


class SessionIdPlugin(object):
    def __init__(self):
        pass

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            req = bottle.request

            req.request_id = str(threading.current_thread().ident) + "-" + str(int(time.time()))

            return callback(*args, **kwargs)

        return wrapper
