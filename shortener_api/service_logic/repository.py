import pybreaker
import redis
import shortener_api.constants as constants


class RedisRepository(object):
    """Simple Redis repository with circuit breaker, is supposed to be injected on startup."""
    def __init__(self, logger, config):
        self._logger = logger
        self._config = config
        self._redis = None
        self._breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

    def save_value(self, key, value):
        """Save key and value to Redis."""
        self._logger.debug("adding value to redis")
        self._breaker.call(self._set_value, key, value)

    def read_value(self, key):
        """Read value by key from Redis and return it as string."""
        self._logger.debug("reading value from redis")
        value = self._breaker.call(self._get_value, key)
        return value.decode() if value else None

    def _set_value(self, key, value):
        if not self._redis:
            self._create_redis()
        self._redis.set(key, value)

    def _get_value(self, key):
        if not self._redis:
            self._create_redis()
        return self._redis.get(key)

    def _create_redis(self):
        self._logger.debug("creating connection to redis server")
        self._redis = redis.StrictRedis(host=self._config[constants.ENV_REDIS_HOST],
                                        port=self._config[constants.ENV_REDIS_PORT], db=0)
