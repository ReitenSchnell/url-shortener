"""Start-up script for the bottle application."""

import logging
import os

import bottle
import shortener_api.constants as constants
import shortener_api.controllers as controllers

from .bottle_plugins.request_id_plugin import SessionIdPlugin
from .exception_handler import ExceptionHandler
from .log_filters import RequestIdFilter, WorkerIdFilter
from .service_logic.repository import RedisRepository
from .service_logic.shortener import Shortener


def init_logger():
    """Create logger and setup its format."""
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
    """Read application configuration from environment variables."""
    variable_names = {
        constants.ENV_BASE_URL: "http://localhost",
        constants.ENV_REDIS_PORT: "8080",
        constants.ENV_REDIS_HOST: "127.0.0.0",
    }
    config = {env_var: os.getenv(env_var, default_value)
              for (env_var, default_value) in variable_names.items()}
    return config


logger = init_logger()
bottle_application = bottle.Bottle()
application = ExceptionHandler(bottle_application, logger)


def setup_application():
    """Create controllers and their dependencies."""
    bottle_application.catchall = False

    config = init_config()
    logging_level = logging.DEBUG
    logger.setLevel(logging_level)
    logger.debug("config contents: {}".format(config))

    bottle_application.install(SessionIdPlugin())

    repository = RedisRepository(logger, config)
    shortener = Shortener(logger, config, repository)

    controller_list = [
        controllers.ErrorController(),
        controllers.ShortenUrlController(logger, config, shortener),
        controllers.RedirectController(logger, config, repository),
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
