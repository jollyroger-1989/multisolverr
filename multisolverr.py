import json
import time
import os
import sys
import logging
import threading
from urllib.parse import urlparse

from flask import Flask, request, Response
import requests

from clients.client import ClientResponse
from clients.flaresolverr import FlareSolverrClient
from clients.scrappey import ScrappeyClient
from clients.directhttp import DirectHTTPClient

# start Flask
app = Flask(__name__)

# debug
DEBUG = os.environ.get('DEBUG', False) != False

# set up logging
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOG_LEVEL)

# configure proxy
http_proxy = os.environ.get('HTTP_PROXY', None)

app.logger.info(http_proxy)
if not http_proxy:
    app.logger.error('HTTP_PROXY must be set')
    sys.exit(1)

os.environ['NO_PROXY'] = '*'

# globals
# cookies are kept per-domain so that credentials for one site are never sent to another
cookieJarsByHost = {}
cookieJarLock = threading.Lock()
lastUserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

VALID_COMMANDS = {'request.get': 'GET', 'request.post': 'POST'}

# setup clients
clients = []
enable_directhttp = os.environ.get('ENABLE_DIRECTHTTP', 'False') != 'False'
enable_flaresolverr = os.environ.get('ENABLE_FLARESOLVERR', 'False') != 'False'
enable_scrappey = os.environ.get('ENABLE_SCRAPPEY', 'False') != 'False'

if enable_directhttp:
    app.logger.info("DirectHTTP enabled")
    clients.append(DirectHTTPClient(http_proxy=http_proxy))

if enable_flaresolverr:
    flaresolverr_url = os.environ.get('FLARESOLVERR_URL', None)
    if not flaresolverr_url:
        app.logger.error('FLARESOLVERR_URL must be set')
        sys.exit(1)
    app.logger.info(f'FlareSolverr enabled / URL: {flaresolverr_url}')
    clients.append(FlareSolverrClient(
        url=flaresolverr_url, http_proxy=http_proxy))

if enable_scrappey:
    scrappey_api_key = os.environ.get('SCRAPPEY_API_KEY', None)
    if not scrappey_api_key:
        app.logger.error('SCRAPPEY_API_KEY must be set')
        sys.exit(1)
    app.logger.info("Scrappey enabled")
    clients.append(ScrappeyClient(scrappey_api_key, http_proxy=http_proxy))

if len(clients) == 0:
    app.logger.error('No clients enabled')
    sys.exit(1)


@app.route("/v1", methods=["POST"])
def v1():
    global lastUserAgent  # pylint: disable=global-statement

    body = request.get_json(silent=True)
    if body is None:
        return Response(status=400, response='{"error": "a JSON body is required"}', content_type='application/json')

    url = body.get('url')
    cmd = body.get('cmd')
    postData = body.get('postData')
    cookies = body.get('cookies')
    maxTimeout = body.get('maxTimeout')

    if not url:
        return Response(status=400, response='{"error": "url is required"}', content_type='application/json')

    if not cmd:
        return Response(status=400, response='{"error": "cmd is required"}', content_type='application/json')

    if cmd not in VALID_COMMANDS:
        return Response(
            status=400,
            response=json.dumps({"error": f"unsupported cmd: {cmd}"}),
            content_type='application/json'
        )

    host = urlparse(url).netloc

    if not postData:
        postData = ''

    if not cookies or len(cookies) == 0:
        with cookieJarLock:
            cookies = list(cookieJarsByHost.get(host, []))

    if not maxTimeout:
        maxTimeout = 60000

    lastResponse = None

    app.logger.info(
        f"{cmd} : {url} / {len(cookies)} cookies / {lastUserAgent}")
    for client in clients:
        if VALID_COMMANDS[cmd] in client.capabilities():
            req = None
            startTimestamp = time.time()
            try:
                if cmd == 'request.get':
                    req = client.get(url, cookies, maxTimeout, lastUserAgent)
                elif cmd == 'request.post':
                    req = client.post(url, postData, cookies,
                                      maxTimeout, lastUserAgent)
            except requests.exceptions.Timeout:
                req = ClientResponse(
                    'error',
                    'Timeout',
                    None
                )
            except (requests.exceptions.RequestException, ValueError) as e:
                req = ClientResponse(
                    'error',
                    str(e),
                    None
                )
            endTimestamp = time.time()
            response = req.toDict()
            response['startTimestamp'] = int(startTimestamp)
            response['endTimestamp'] = int(endTimestamp)

            lastResponse = response
            lastUserAgent = (response.get('solution', {}) or {}
                             ).get('userAgent', lastUserAgent) or lastUserAgent
            if response['status'] == 'ok':
                with cookieJarLock:
                    jar = cookieJarsByHost.setdefault(host, [])
                    for cookie in response['solution'].get('cookies', []) or []:
                        for i in range(len(jar)):
                            if jar[i]['name'] == cookie['name']:
                                jar[i] = cookie
                                break
                        else:
                            jar.append(cookie)
                app.logger.info(
                    f" -> client {client.__class__.__name__} succeeded.")
                app.logger.debug(
                    f" -> response: {response['solution']['response']}")
                return Response(
                    response=json.dumps(response),
                    content_type='application/json'
                )

            app.logger.info(f" -> client {client.__class__.__name__} failed.")

    return Response(
        response=json.dumps(lastResponse),
        content_type='application/json'
    )


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=8191)
