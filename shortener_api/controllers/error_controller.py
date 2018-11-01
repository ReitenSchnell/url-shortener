import bottle
from shortener_api.constants import UNHANDLED_ERROR_TEXT


class ErrorController(object):
    """Controller for responding with HTTP 500 status code in case of unhandled error."""
    def __init__(self):
        pass

    def get_routes(self):
        return [
            {
                "path": "/error",
                "method": "GET",
                "callback": self.get_error_response
            }
        ]

    def get_error_response(self):
        """Read latest error and return it inside HTTP response."""
        error_text = bottle.request.environ.get("error_text", UNHANDLED_ERROR_TEXT)
        error_json = {
            "error": error_text
        }
        return bottle.HTTPResponse(status=500, body=error_json)
