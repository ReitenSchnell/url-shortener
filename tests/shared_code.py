import logging

import shortener_api
import webtest


def get_null_log():
    null_logg = logging.getLogger("")
    null_logg.setLevel(logging.NOTSET)
    return null_logg


def setup_application():
    shortener_api.setup_application()
    application = webtest.TestApp(shortener_api.application)
    return application
