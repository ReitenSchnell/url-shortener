from shortener_api.service_logic.repository import RedisRepository
from shortener_api.service_logic.shortener import Shortener
from tests.shared_code import get_null_log

SERVICE_URL = "http://service.com/"
URL_HASHER_PATH = "shortener_api.service_logic.url_hasher.UrlHasher.get_hashed_url"


def test_returns_service_url_extended_with_code(mocker):
    test_config = {
        "ENV_BASE_URL": SERVICE_URL
    }
    hashed_code = "FooBar123"
    hasher_mock = mocker.patch(URL_HASHER_PATH, return_value=hashed_code)
    test_log = get_null_log()
    repository = RedisRepository(test_log, test_config)
    shortener = Shortener(test_log, test_config, repository)
    original_url = "some url"

    result = shortener.create_shortened_url(original_url)

    assert SERVICE_URL + hashed_code == result
    hasher_mock.assert_called_once_with(original_url)
