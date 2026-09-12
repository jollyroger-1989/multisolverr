import os
import sys

import yaml

from clients.byparr import ByparrClient
from clients.directhttp import DirectHTTPClient
from clients.flaresolverr import FlareSolverrClient
from clients.scrappey import ScrappeyClient

CLIENT_TYPES = {
    'direct': DirectHTTPClient,
    'flaresolverr': FlareSolverrClient,
    'byparr': ByparrClient,
    'scrappey': ScrappeyClient,
}


def _buildClient(step, http_proxy, logger):
    solver_type = step.get('type')
    client_cls = CLIENT_TYPES.get(solver_type)
    if client_cls is None:
        logger.error(
            f"Unknown solver type '{solver_type}'. Valid types: {', '.join(CLIENT_TYPES)}")
        sys.exit(1)

    if solver_type == 'direct':
        return client_cls(http_proxy=http_proxy)

    if solver_type in ('flaresolverr', 'byparr'):
        url = step.get('url')
        if not url:
            logger.error(f"Pipeline step '{solver_type}' requires a 'url'")
            sys.exit(1)
        return client_cls(url=url, http_proxy=http_proxy)

    if solver_type == 'scrappey':
        api_key = step.get('api_key')
        if not api_key:
            logger.error("Pipeline step 'scrappey' requires an 'api_key'")
            sys.exit(1)
        return client_cls(api_key, http_proxy=http_proxy)

    raise AssertionError(f"unhandled solver type: {solver_type}")


def loadPipeline(config_path, http_proxy, logger):
    if not os.path.isfile(config_path):
        logger.error(f"Pipeline config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, encoding='utf-8') as f:
        # allows secrets (e.g. api keys) to be injected from the environment
        # instead of being hardcoded in the pipeline file
        raw = os.path.expandvars(f.read())

    config = yaml.safe_load(raw) or {}
    steps = config.get('pipeline')
    if not steps:
        logger.error(f"No 'pipeline' defined in {config_path}")
        sys.exit(1)

    return [_buildClient(step, http_proxy, logger) for step in steps]
