import base64
import hashlib
import uuid

from shortener_api.constants import CODE_LENGTH


class UrlHasher(object):
    def __init__(self, logger):
        self._logger = logger

    def get_hashed_url(self, url):
        salt = uuid.uuid4()
        encoding = "utf-8"
        salted_url = "{}{}".format(url, salt).encode(encoding)
        hasher = hashlib.sha256(salted_url)
        hashed_url = base64.urlsafe_b64encode(hasher.digest()).decode(encoding)
        short_code = hashed_url[0:CODE_LENGTH]
        self._logger.debug("hashed url is {}".format(short_code))
        return short_code
