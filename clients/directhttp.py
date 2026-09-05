from curl_cffi import requests

from .client import Client, ClientResponse, Solution


def _impersonateFor(userAgent):
    ua = userAgent or ''
    isMobile = 'Mobile' in ua or 'Android' in ua or 'iPhone' in ua or 'iPad' in ua
    if 'Edg/' in ua:
        return 'edge'
    if 'Firefox/' in ua:
        return 'firefox'
    if 'Chrome/' in ua:
        return 'chrome_android' if 'Android' in ua else 'chrome'
    if 'Safari/' in ua:
        return 'safari_ios' if isMobile else 'safari'
    return 'chrome'


class DirectHTTPClient(Client):
    def __init__(self, http_proxy=None):
        super().__init__()
        self.proxies = {
            'http': http_proxy,
            'https': http_proxy
        }

    def _parseResponse(self, req, userAgent, cookies):
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
                cookies + [
                    {'name': c.name, 'value': c.value,
                     'domain': c.domain, 'path': c.path, 'expires': c.expires}
                    for c in req.cookies.jar
                ],
                userAgent,
                dict(req.headers)
            )
        )

    def capabilities(self):
        return ['GET', 'POST']

    def get(self, url, cookies=None, maxTimeout=60000, userAgent=None):
        cookies = cookies or []
        req = requests.get(url,
                           cookies=dict(
                               map(lambda k: [k['name'], k['value']], cookies)),
                           timeout=maxTimeout,
                           proxies=self.proxies,
                           headers={
                               'User-Agent': userAgent
                           },
                           impersonate=_impersonateFor(userAgent)
                           )
        return self._parseResponse(req, userAgent, cookies)

    def post(self, url, postData="", cookies=None, maxTimeout=60000, userAgent=None):
        cookies = cookies or []
        req = requests.post(url,
                            data=postData,
                            cookies=dict(
                                map(lambda k: [k['name'], k['value']], cookies)),
                            timeout=maxTimeout,
                            proxies=self.proxies,
                            headers={
                                'User-Agent': userAgent
                            },
                            impersonate=_impersonateFor(userAgent)
                            )
        return self._parseResponse(req, userAgent, cookies)
