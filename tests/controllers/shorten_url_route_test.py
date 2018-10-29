import json

import tests.shared_code as shared

SHORTENER_PATH = "shortener_api.service_logic.shortener.Shortener.create_shortened_url"


def test_returns_201_status_on_valid_input(mocker):
    mocker.patch(SHORTENER_PATH, return_value="foo")
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {"url": "http://google.com"}

    resp = application.post("/shorten_url", json.dumps(body), headers=headers)

    assert 201 == resp.status_code


def test_returns_shortened_url_in_response_body(mocker):
    shortened_url = "foo"
    mocker.patch(SHORTENER_PATH, return_value=shortened_url)
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {"url": "http://google.com"}

    resp = application.post("/shorten_url", json.dumps(body), headers=headers)

    assert shortened_url == resp.json["shortened_url"]


def test_returns_400_status_on_invalid_input(mocker):
    shortener = mocker.patch(SHORTENER_PATH)
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {}

    resp = application.post("/shorten_url", json.dumps(body), headers=headers, expect_errors=True)

    assert 400 == resp.status_code
    assert 0 == shortener.call_count


def test_returns_400_status_on_invalid_original_url(mocker):
    shortener = mocker.patch(SHORTENER_PATH)
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {"url": "some url"}

    resp = application.post("/shorten_url", json.dumps(body), headers=headers, expect_errors=True)

    assert 400 == resp.status_code
    assert 0 == shortener.call_count
