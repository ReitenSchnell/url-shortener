import pybreaker
import pytest
import redis
import shortener_api.constants as constants
from shortener_api.service_logic.repository import RedisRepository
from tests.shared_code import get_null_log

REDIS_CREATE_PATH = "redis.StrictRedis.__init__"
REDIS_GET_PATH = "redis.StrictRedis.get"
REDIS_SET_PATH = "redis.StrictRedis.set"
REDIS_HOST = "host"
REDIS_PORT = "port"
CONFIG = {
    constants.ENV_REDIS_HOST: REDIS_HOST,
    constants.ENV_REDIS_PORT: REDIS_PORT,
}


def test_should_create_redis_client_with_correct_parameters(mocker):
    strict_redis_mock = mocker.patch(REDIS_CREATE_PATH, return_value=None)
    mocker.patch(REDIS_GET_PATH)
    repository = RedisRepository(get_null_log(), CONFIG)

    repository.read_value("key")

    strict_redis_mock.assert_called_once_with(host=REDIS_HOST, port=REDIS_PORT, db=0)


def test_should_store_key_to_redis(mocker):
    mocker.patch(REDIS_CREATE_PATH, return_value=None)
    redis_mock = mocker.patch(REDIS_SET_PATH)
    repository = RedisRepository(get_null_log(), CONFIG)
    key = "some key"
    value = "some value"

    repository.save_value(key, value)

    redis_mock.assert_called_once_with(key, value)


def test_should_read_key_from_redis(mocker):
    mocker.patch(REDIS_CREATE_PATH, return_value=None)
    value = "some value"
    redis_mock = mocker.patch(REDIS_GET_PATH, return_value=value.encode())
    repository = RedisRepository(get_null_log(), CONFIG)
    key = "some key"

    result = repository.read_value(key)

    assert value == result
    redis_mock.assert_called_once_with(key)


def test_should_read_key_from_redis_and_return_none_if_not_found(mocker):
    mocker.patch(REDIS_CREATE_PATH, return_value=None)
    redis_mock = mocker.patch(REDIS_GET_PATH, return_value=None)
    repository = RedisRepository(get_null_log(), CONFIG)
    key = "some key"

    result = repository.read_value(key)

    assert result is None
    redis_mock.assert_called_once_with(key)


def test_should_throw_breaker_error_and_not_call_redis_after_three_fails_on_write(mocker):
    mocker.patch(REDIS_CREATE_PATH, return_value=None)
    redis_mock = mocker.patch(REDIS_SET_PATH)
    redis_mock.side_effect = [redis.TimeoutError(), redis.TimeoutError(), redis.TimeoutError()]
    repository = RedisRepository(get_null_log(), CONFIG)

    for _ in range(2):
        with pytest.raises(redis.TimeoutError):
            repository.save_value("key", "value")
    for _ in range(2):
        with pytest.raises(pybreaker.CircuitBreakerError):
            repository.save_value("key", "value")

    assert 3 == redis_mock.call_count


def test_should_throw_breaker_error_and_not_call_redis_after_three_fails_on_read(mocker):
    mocker.patch(REDIS_CREATE_PATH, return_value=None)
    redis_mock = mocker.patch(REDIS_GET_PATH)
    redis_mock.side_effect = [redis.TimeoutError(), redis.TimeoutError(), redis.TimeoutError()]
    repository = RedisRepository(get_null_log(), CONFIG)

    for _ in range(2):
        with pytest.raises(redis.TimeoutError):
            repository.read_value("key")
    for _ in range(2):
        with pytest.raises(pybreaker.CircuitBreakerError):
            repository.read_value("key")

    assert 3 == redis_mock.call_count
