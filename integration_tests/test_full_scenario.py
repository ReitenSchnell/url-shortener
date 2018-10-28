import requests

SERVICE_BASE_ADDRESS = "http://localhost:8000"
SHORTEN_ROUTE = "/shorten_url"


# reurns 201
# returns full url + code of expected length
# never returns same result
# goes to correct link

def test_returns_shortened_url_and_201_status():
    request_body = {"url": "http://some.com"}

    result = requests.post(SERVICE_BASE_ADDRESS + SHORTEN_ROUTE, json=request_body)

    assert 201 == result.status_code


def test_redirects_to_full_url():
    result = requests.get(SERVICE_BASE_ADDRESS + "/foo")

    assert "http://www.google.com/" == result.url
