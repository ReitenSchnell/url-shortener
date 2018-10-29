from shortener_api.constants import ENV_BASE_URL
from shortener_api.service_logic.url_hasher import UrlHasher


class Shortener(object):
    def __init__(self, logger, config, repository):
        self._logger = logger
        self._config = config
        self._repository = repository

    def create_shortened_url(self, original_url):
        self._logger.debug("starting to create shortened version of {}".format(original_url))
        hasher = UrlHasher(self._logger)
        hashed_url = hasher.get_hashed_url(original_url)
        shortened_url = self._config[ENV_BASE_URL] + hashed_url
        return shortened_url
