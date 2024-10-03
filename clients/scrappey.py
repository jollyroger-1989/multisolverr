import requests
import json
from .client import Client, ClientResponse, Solution


class ScrappeyClient(Client):
    def __init__(self, apiKey, http_proxy=None):
        super().__init__()
        self.proxy = http_proxy
        self.url = f"https://publisher.scrappey.com/api/v1?key={apiKey}"

    def _parseResponse(self, req, userAgent):
        if req.status_code != 200:
            return ClientResponse(
                'error',
                f"STATUS: {req.status_code} TEXT: {req.text}",
                None
            )

        resp = req.json()
        return ClientResponse(
            'ok' if resp.get('data', 'error') == 'success' else 'error',
            resp.get('message', ''),
            Solution(
                resp.get('solution', {}).get('currentUrl', None),
                resp.get('solution', {}).get('statusCode', None) or 200,
                resp.get('solution', {}).get('response', None),
                resp.get('solution', {}).get('cookies', None),
                resp.get('solution', {}).get(
                    'requestHeaders', {}).get('user-agent', None) or
                resp.get('solution', {}).get(
                    'requestHeaders', {}).get('User-Agent', None) or
                resp.get('solution', {}).get('userAgent', None) or
                userAgent
            )
        )

    def capabilities(self):
        return ['GET', 'POST']

    def get(self, url, cookies=[], maxTimeout=60000, userAgent=None):
        paylod = {
            'cmd': 'request.get',
            'url': url,
            'cookiejar': cookies,
            'proxy': self.proxy,
            'customHeaders': {
                'user-agent': userAgent,
                'User-Agent': userAgent
            }
        }
        req = requests.post(self.url, timeout=maxTimeout, json=paylod)
        return self._parseResponse(req, userAgent)

    def post(self, url, postData="", cookies=[], maxTimeout=60000, userAgent=None):
        paylod = {
            'cmd': 'request.post',
            'url': url,
            'postData': postData,
            'cookiejar': cookies,
            'proxy': self.proxy,
            'customHeaders': {
                'user-agent': userAgent,
                'User-Agent': userAgent
            }
        }
        req = requests.post(self.url, timeout=maxTimeout, json=paylod)
        return self._parseResponse(req, userAgent)
