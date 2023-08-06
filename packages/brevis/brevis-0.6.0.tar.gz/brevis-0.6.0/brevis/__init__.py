import logging

import requests

logger = logging.getLogger(__name__)


class BrevisClient(object):
    def __init__(self, base_url="http://localhost:1323", session=None, timeout=None):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.timeout = timeout

    def _make_request(self, method, endpoint, data):
        url = "{}{}".format(self.base_url, endpoint)
        r = requests.Request(method=method, url=url, json=data)
        p = r.prepare()
        resp = self.session.send(p, timeout=self.timeout)

        if resp is None:
            msg = "Couldn't connect to '{}'".format(url)
            logger.critical(msg)
            raise requests.RequestException(msg)

        if resp.status_code < 400:
            try:
                return resp.json()
            except Exception as e:
                if resp.text:
                    logger.error("Unhandled error {} while parsing JSON response: {}".format(str(e), resp.text))
                else:
                    return ""
        else:
            msg = "Got status code '{}' doing a '{}' to '{}' with body '{}".format(
                resp.status_code, method, resp.url, resp.text)
            logger.critical(msg)
            resp.raise_for_status()

    def health(self):
        return self._make_request("GET", "/", None)

    def stats(self, id_):
        return self._make_request("GET", "/{}/stats".format(id_), None)

    def shorten(self, url):
        data = {"url": url}
        return self._make_request("POST", "/shorten", data)

    def unshorten(self, short_url):
        if short_url.startswith(self.base_url):
            try:
                short_url = short_url.rsplit("/", 1)[1]
            except IndexError:
                pass
        data = {"short_url": short_url}
        return self._make_request("POST", "/unshorten", data)
