import bottle


class RedirectController(object):
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
        self._logger.debug("found full url for {}".format(short_code))
        return bottle.redirect("http://google.com", 301)
