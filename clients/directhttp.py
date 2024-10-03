import requests

from .client import Client, ClientResponse, Solution


class DirectHTTPClient(Client):
    def __init__(self, http_proxy=None):
        super().__init__()
        self.proxies = {
            'http': http_proxy,
            'https': http_proxy
        }

    def _parseResponse(self, req, userAgent):
        if req.status_code != 200:
            return ClientResponse(
                'error',
                f"STATUS: {req.status_code} TEXT: {req.text}",
                None
            )

        return ClientResponse(
            'ok',
            '',
            Solution(
                req.url,
                req.status_code,
                req.text,
                [
                    {'name': c.name, 'value': c.value,
                     'domain': c.domain, 'path': c.path, 'expires': c.expires}
                    for c in req.cookies
                ],
                userAgent
            )
        )

    def capabilities(self):
        return ['GET', 'POST']

    def get(self, url, cookies=[], maxTimeout=60000, userAgent=None):
        req = requests.get(url,
                           cookies=dict(
                               map(lambda k: [k['name'], k['value']], cookies)),
                           timeout=maxTimeout,
                           proxies=self.proxies,
                           headers={
                               'User-Agent': userAgent
                           }
                           )
        return self._parseResponse(req, userAgent)

    def post(self, url, postData="", cookies=[], maxTimeout=60000, userAgent=None):
        req = requests.post(url,
                            data=postData,
                            cookies=dict(
                                map(lambda k: [k['name'], k['value']], cookies)),
                            timeout=maxTimeout,
                            proxies=self.proxies,
                            headers={
                                'User-Agent': userAgent
                            }
                            )
        return self._parseResponse(req, userAgent)
