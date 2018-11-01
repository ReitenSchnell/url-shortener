from shortener_api.constants import ENV_BASE_URL
from shortener_api.service_logic.url_hasher import UrlHasher


class Shortener(object):
    def __init__(self, logger, config, repository):
        self._logger = logger
        self._config = config
        self._repository = repository

    def create_shortened_url(self, original_url):
        """Perform URL hashing, store the result along with original URL and return shortened URL."""
        self._logger.debug("starting to create shortened version of {}".format(original_url))
        hasher = UrlHasher(self._logger)
        hashed_code = hasher.get_hashed_url(original_url)
        # we want to avoid collisions and check if the code was previously stored
        while self._repository.read_value(hashed_code):
            hashed_code = hasher.get_hashed_url(original_url)

        full_shortened_url = self._config[ENV_BASE_URL] + hashed_code
        self._logger.debug("shortened url is {}".format(full_shortened_url))
        self._repository.save_value(hashed_code, original_url)
        return full_shortened_url
