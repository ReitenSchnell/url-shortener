"""Integration tests for URL shortener. Should be run against service hosted in Docker."""
import requests

SERVICE_BASE_ADDRESS = "http://localhost:8000"
SHORTEN_ROUTE = "/shorten_url"


def test_returns_shortened_url_and_201_status():
    request_body = {"url": "http://some.com"}

    result = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)

    assert 201 == result.status_code
    assert result.json()["shortened_url"]


def test_shortened_url_contains_base_url_and_code_of_expected_length():
    request_body = {"url": "http://some.com"}

    result = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)

    full_url = result.json()["shortened_url"]
    short_code = full_url[len(SERVICE_BASE_ADDRESS) + 1:]
    assert SERVICE_BASE_ADDRESS in full_url
    assert 8 == len(short_code)


def test_returns_different_shortened_urls_in_response_to_same_original_url():
    request_body = {"url": "http://some.com"}

    result1 = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)
    result2 = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)

    assert result1.json()["shortened_url"] != result2.json()["shortened_url"]


def test_redirects_to_original_url():
    original_url = "https://www.babylonhealth.com/"
    request_body = {"url": original_url}
    shortened_response = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)

    result = requests.get(shortened_response.json()["shortened_url"])

    assert original_url == result.url
