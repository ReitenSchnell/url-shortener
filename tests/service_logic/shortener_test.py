from shortener_api.service_logic.repository import RedisRepository
from shortener_api.service_logic.shortener import Shortener
from tests.shared_code import get_null_log

SERVICE_URL = "http://service.com/"
TEST_CONFIG = {"ENV_BASE_URL": SERVICE_URL}
HASHED_CODE = "FooBar123"
ORIGINAL_URL = "some url"
URL_HASHER_PATH = "shortener_api.service_logic.url_hasher.UrlHasher.get_hashed_url"
REPOSITORY_WRITE_PATH = "shortener_api.service_logic.repository.RedisRepository.save_value"
REPOSITORY_READ_PATH = "shortener_api.service_logic.repository.RedisRepository.read_value"


def test_returns_service_url_extended_with_code(mocker):
    hasher_mock = mocker.patch(URL_HASHER_PATH, return_value=HASHED_CODE)
    mocker.patch(REPOSITORY_WRITE_PATH)
    mocker.patch(REPOSITORY_READ_PATH, return_value=None)
    test_log = get_null_log()
    repository = RedisRepository(test_log, TEST_CONFIG)
    shortener = Shortener(test_log, TEST_CONFIG, repository)

    result = shortener.create_shortened_url(ORIGINAL_URL)

    assert SERVICE_URL + HASHED_CODE == result
    hasher_mock.assert_called_once_with(ORIGINAL_URL)


def test_saves_original_and_shortened_url_to_repository(mocker):
    mocker.patch(URL_HASHER_PATH, return_value=HASHED_CODE)
    mocker.patch(REPOSITORY_READ_PATH, return_value=None)
    repository_mock = mocker.patch(REPOSITORY_WRITE_PATH)
    test_log = get_null_log()
    repository = RedisRepository(test_log, TEST_CONFIG)
    shortener = Shortener(test_log, TEST_CONFIG, repository)

    shortener.create_shortened_url(ORIGINAL_URL)

    repository_mock.assert_called_once_with(HASHED_CODE, ORIGINAL_URL)


def test_regenerates_and_stores_hash_code_if_it_already_taken(mocker):
    hasher_mock = mocker.patch(URL_HASHER_PATH)
    hasher_mock.side_effect = ["hash1", "hash2", "hash3"]
    repository_read_mock = mocker.patch(REPOSITORY_READ_PATH)
    repository_read_mock.side_effect = ["url1", "url2", None]
    repository_mock = mocker.patch(REPOSITORY_WRITE_PATH)
    test_log = get_null_log()
    repository = RedisRepository(test_log, TEST_CONFIG)
    shortener = Shortener(test_log, TEST_CONFIG, repository)

    shortener.create_shortened_url(ORIGINAL_URL)

    assert 3 == hasher_mock.call_count
    assert 3 == repository_read_mock.call_count
    repository_mock.assert_called_once_with("hash3", ORIGINAL_URL)
