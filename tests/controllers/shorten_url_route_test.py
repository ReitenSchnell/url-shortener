import tests.shared_code as shared


def test_returns_201_status():
    application = shared.setup_application()
    resp = application.post("/shorten_url")
    assert 201 == resp.status_code
