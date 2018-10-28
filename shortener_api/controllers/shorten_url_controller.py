import bottle


class ShortenUrlController(object):
    def __init__(self):
        pass

    def get_routes(self):
        return [
            {
                "path": "/shorten_url",
                "method": "POST",
                "callback": self.post_url
            }
        ]

    def post_url(self):
        return bottle.HTTPResponse(status=201)
