from shortener_api.constants import UNHANDLED_ERROR_TEXT
import tests.shared_code as shared


def test_returns_500_status():
    application = shared.setup_application()
    resp = application.get("/error", expect_errors=500)
    assert 500 == resp.status_code


def test_returns_error():
    application = shared.setup_application()
    resp = application.get("/error", expect_errors=500)
    assert UNHANDLED_ERROR_TEXT == resp.json["error"]
