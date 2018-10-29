from shortener_api.constants import CODE_LENGTH
from shortener_api.service_logic.url_hasher import UrlHasher
from tests.shared_code import get_null_log


def test_returns_different_results_for_same_input():
    hasher = UrlHasher(get_null_log())
    url = "https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags"

    result1 = hasher.get_hashed_url(url)
    result2 = hasher.get_hashed_url(url)

    assert result1 != result2


def test_returns_short_code_of_expected_length():
    hasher = UrlHasher(get_null_log())
    url = "https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags"

    result = hasher.get_hashed_url(url)

    assert CODE_LENGTH == len(result)
