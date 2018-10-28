import logging
import os

import bottle
import shortener_api.constants as constants
import shortener_api.controllers as controllers

from .bottle_plugins.request_id_plugin import SessionIdPlugin
from .exception_handler import ExceptionHandler
from .log_filters import RequestIdFilter, WorkerIdFilter


def init_logger():
    service_logger = logging.getLogger(constants.APP_NAME)
    service_logger.addFilter(RequestIdFilter())
    service_logger.addFilter(WorkerIdFilter())
    handler = logging.StreamHandler()
    formatter = logging.Formatter(constants.LOG_FORMAT)
    handler.setFormatter(formatter)
    service_logger.addHandler(handler)

    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.CRITICAL)

    return service_logger


def init_config():
    variable_names = {
        constants.ENV_BASE_URL: "http://localhost/"
    }
    config = {env_var: os.getenv(env_var, default_value)
              for (env_var, default_value) in variable_names.items()}
    return config


logger = init_logger()
bottle_application = bottle.Bottle()
application = ExceptionHandler(bottle_application, logger)


def setup_application():
    bottle_application.catchall = False

    config = init_config()
    logging_level = logging.DEBUG
    logger.setLevel(logging_level)
    logger.debug("config contents: {}".format(config))

    bottle_application.install(SessionIdPlugin())

    controller_list = [
        controllers.ErrorController(),
        controllers.ShortenUrlController()
    ]

    for controller in controller_list:
        for route in controller.get_routes():
            logger.debug("initializing route: {}".format(route))
            bottle_application.route(**route)


try:
    import uwsgidecorators

    uwsgidecorators.postfork(setup_application)
except ImportError:
    logger.info("NOT RUNNING ON UWSGI")
