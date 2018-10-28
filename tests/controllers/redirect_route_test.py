import tests.shared_code as shared


def test_returns_301_status_on_found_url():
    application = shared.setup_application()
    resp = application.get("/some")
    assert 301 == resp.status_code


def test_returns_redirect_location_on_found_url():
    application = shared.setup_application()
    resp = application.get("/some")
    assert "http://google.com" == resp.location
