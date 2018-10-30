import tests.shared_code as shared

REPOSITORY_PATH = "shortener_api.service_logic.repository.RedisRepository.read_value"


def test_returns_301_status_on_found_url(mocker):
    repository_mock = mocker.patch(REPOSITORY_PATH, return_value="http://reddit.com")
    application = shared.setup_application()
    short_code = "AbcdEF"

    resp = application.get("/" + short_code)

    assert 301 == resp.status_code
    repository_mock.assert_called_once_with(short_code)


def test_returns_redirect_location_on_found_url(mocker):
    full_url = "http://reddit.com"
    mocker.patch(REPOSITORY_PATH, return_value=full_url)
    application = shared.setup_application()

    resp = application.get("/AbcdEF")

    assert full_url == resp.location


def test_returns_404_on_not_found_url(mocker):
    repository_mock = mocker.patch(REPOSITORY_PATH, return_value=None)
    application = shared.setup_application()
    short_code = "AbcdEF"

    resp = application.get("/" + short_code, expect_errors=True)

    assert 404 == resp.status_code
    repository_mock.assert_called_once_with(short_code)
