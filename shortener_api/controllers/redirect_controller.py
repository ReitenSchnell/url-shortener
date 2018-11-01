import bottle


class RedirectController(object):
    """Controller that is responsible for redirection to original URL on GET request."""
    def __init__(self, logger, config, repository):
        self._logger = logger
        self._config = config
        self._repository = repository

    def get_routes(self):
        return [
            {
                "path": "/<short_code>",
                "method": "GET",
                "callback": self.redirect_to_full_url
            }
        ]

    def redirect_to_full_url(self, short_code):
        """Find original URL by its short code and redirect user to the URL."""
        full_url = self._repository.read_value(short_code)
        if not full_url:
            error_text = "full url by short code {} is not found".format(short_code)
            self._logger.warn(error_text)
            return bottle.HTTPResponse(status=404, body={"error": error_text})

        self._logger.debug("found full url for {}: {}".format(short_code, full_url))
        return bottle.redirect(full_url, 301)
