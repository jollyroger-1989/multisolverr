# MultiSolverr

## Compatibility

The api is partially compatible with the [Flaresolverr](https://FlareSolverr/FlareSolverr) API.  
That's enough to use it with [Prowlarr](https://prowlarr.com/).  
**Not tested with Jackett.**

## Functionality

MultiSolverr is a simple API that can be used to solve Cloudflare challenges. It supports multiple solvers, including DirectHTTP, FlareSolverr, and Scrappey.
It will try to solve the challenge with the solvers in the order defined in the [pipeline config file](#configure-solvers), and return the response from the first one that succeeds.

## Installation

Copy [`pipeline.example.yml`](pipeline.example.yml) to `pipeline.yml`, edit it to
pick which solvers to use and in which order, then mount it in your
`docker-compose.yml` file:

```yaml
multisolverr:
  image: ghcr.io/jollyroger-1989/multisolverr:latest
  environment:
    - HTTP_PROXY=http://user@password:proxy:3128
    - SCRAPPEY_API_KEY=YOUR_API_KEY
  volumes:
    - ./pipeline.yml:/app/pipeline.yml:ro
```

**The HTTP_PROXY config is mandotary. The use of [squid](https://hub.docker.com/r/ubuntu/squid) is recommended.**

## Solvers

### DirectHTTP

DirectHTTP is a simple solver that uses the requests library to fetch the page and return the content.

### FlareSolverr

FlareSolverr is a solver that uses the [Flaresolverr](https://FlareSolverr/FlareSolverr) API to solve Cloudflare challenges.

### Scrappey

Scrappey is a solver that uses the [Scrappey](https://scrappey.com/) API to solve Cloudflare challenges.


## Configure solvers

The pipeline (which solvers to use, and in which order) is defined in a YAML
file, `pipeline.yml` by default (override the path with the `PIPELINE_CONFIG`
environment variable). Each solver is tried in order until one succeeds:

```yaml
pipeline:
  - type: direct

  - type: flaresolverr
    url: http://flaresolverr:8191/v1

  - type: scrappey
    api_key: ${SCRAPPEY_API_KEY}
```

Values support `${VAR}` interpolation from the environment, so secrets like
API keys don't need to be hardcoded in the file.

| Solver | `type` | Required fields |
| --- | --- | --- |
| DirectHTTP | `direct` | |
| FlareSolverr | `flaresolverr` | `url`: FlareSolverr API URL |
| Scrappey | `scrappey` | `api_key`: Scrappey API key |

## Configure Prowlarr

Configure this service as a FlareSolverr service in Prowlarr.