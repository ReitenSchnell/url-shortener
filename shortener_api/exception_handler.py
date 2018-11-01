class ExceptionHandler(object):
    """Middleware for the bottle application."""
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger

    def __call__(self, environ, start_response):
        """Catch all unhandled exceptions and redirect to special error-handling route."""
        try:
            return self.app(environ, start_response)
        except Exception as ex:
            self.logger.exception("unhandled error occurred: {}".format(ex))
            environ["PATH_INFO"] = "/error"
            environ["error_text"] = str(ex)
            return self.app(environ, start_response)
