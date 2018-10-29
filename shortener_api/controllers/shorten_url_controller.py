import bottle
import validators


class ShortenUrlController(object):
    def __init__(self, logger, config, shortener):
        self._logger = logger
        self._config = config
        self._shortener = shortener

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
            malformed_body_error = "request body is malformed"
            self._logger.warn(malformed_body_error)
            return bottle.HTTPResponse(status=400, data=malformed_body_error)

        original_url = bottle.request.json["url"]
        if not validators.url(original_url):
            invalid_url_error = "original url {} is not valid".format(original_url)
            self._logger.warn(invalid_url_error)
            return bottle.HTTPResponse(status=400, data=invalid_url_error)

        shortened_url = self._shortener.create_shortened_url(original_url)
        result = {
            "shortened_url": shortened_url
        }
        return bottle.HTTPResponse(status=201, body=result)
