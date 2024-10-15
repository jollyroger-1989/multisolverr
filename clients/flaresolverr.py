import requests

from .client import Client, ClientResponse, Solution


class FlareSolverrClient(Client):
    def __init__(self, url='http://flaresolverr:8191/v1', http_proxy=None):
        super().__init__()
        self.url = url
        self.proxy = http_proxy

    def _parseResponse(self, req):
        if req.status_code != 200:
            return ClientResponse(
                'error',
                f"STATUS: {req.status_code} TEXT: {req.text}",
                None
            )

        resp = req.json()
        return ClientResponse(
            resp.get('status', 'nok'),
            resp.get('message', ''),
            Solution(
                resp.get('solution', {}).get('url', None),
                resp.get('solution', {}).get('status', None),
                resp.get('solution', {}).get('response', None),
                resp.get('solution', {}).get('cookies', None),
                resp.get('solution', {}).get('userAgent', None)
            )
        )

    def capabilities(self):
        return ['GET', 'POST']

    def get(self, url, cookies=[], maxTimeout=60000, userAgent=None):
        req = requests.post(self.url, timeout=maxTimeout, json={
            'cmd': 'request.get',
            'url': url,
            'maxTimeout': maxTimeout,
            'cookies': cookies
        })
        return self._parseResponse(req)

    def post(self, url, postData="", cookies=[], maxTimeout=60000, userAgent=None):
        req = requests.post(self.url, timeout=maxTimeout, json={
            'cmd': 'request.post',
            'url': url,
            'maxTimeout': maxTimeout,
            'postData': postData,
            'cookies': cookies
        })
        return self._parseResponse(req)
