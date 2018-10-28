import json

import tests.shared_code as shared


def test_returns_201_status_on_valid_input():
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {"url": "http://google.com"}
    resp = application.post("/shorten_url", json.dumps(body), headers=headers)
    assert 201 == resp.status_code


def test_returns_400_status_on_invalid_input():
    application = shared.setup_application()
    headers = {"Content-Type": "application/json"}
    body = {}
    resp = application.post("/shorten_url", json.dumps(body), headers=headers, expect_errors=True)
    assert 400 == resp.status_code
