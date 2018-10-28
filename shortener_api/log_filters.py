import logging

import bottle


class RequestIdFilter(logging.Filter):
    @staticmethod
    def get_request_id(default=None):
        try:
            return bottle.request.request_id
        except (RuntimeError, TypeError, KeyError, AttributeError):
            # Bottle request might be not yet initialized. Depending on
            # initialisation state, Bottle can raise any of the above errors.
            return default

    def filter(self, record):
        record.request_id = self.get_request_id()
        return super().filter(record)


class WorkerIdFilter(logging.Filter):
    def filter(self, record):
        record.worker_id = 0
        try:
            import uwsgi
            record.worker_id = uwsgi.worker_id()
        except ImportError:
            pass
        return True
