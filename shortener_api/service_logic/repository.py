class RedisRepository(object):
    def __init__(self, logger, config):
        self._logger = logger
        self._config = config
