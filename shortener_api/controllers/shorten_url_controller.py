import bottle
from shortener_api.constants import ENV_BASE_URL


class ShortenUrlController(object):
    def __init__(self, logger, config, repository):
        self._logger = logger
        self._config = config
        self._repository = repository

    def get_routes(self):
        return [
            {
                "path": "/shorten_url",
                "method": "POST",
                "callback": self.post_url
            }
        ]

    def post_url(self):
        if "url" not in bottle.request.json:
            return bottle.HTTPResponse(status=400)
        url_to_shorten = bottle.request.json["url"]
        self._logger.debug("created short url for {}".format(url_to_shorten))
        hashed_url = "foo"
        shortened_url = "{}{}".format(self._config[ENV_BASE_URL], hashed_url)
        result = {
            "shortened_url": shortened_url
        }
        return bottle.HTTPResponse(status=201, body=result)
