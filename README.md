# MultiSolverr

## Compatibility

The api is partially compatible with the [Flaresolverr](https://FlareSolverr/FlareSolverr) API.  
That's enough to use it with [Prowlarr](https://prowlarr.com/).  
**Not tested with Jackett.**

## Functionality

MultiSolverr is a simple API that can be used to solve Cloudflare challenges. It supports multiple solvers, including DirectHTTP, FlareSolverr, and Scrappey.
It wil try to solve the challenge with the solvers in the following order:

1. DirectHTTP
2. FlareSolverr
3. Scrappey

It will return the response from the first solver that successfully solves the challenge.

## Installation

Add the following to your `docker-compose.yml` file:

```yaml
multisolverr:
  image: ghcr.io/jollyroger-1989/multisolverr:latest
  environment:
    - ENABLE_DIRECTHTTP=True
    - ENABLE_FLARESOLVERR=True
    - FLARESOLVERR_URL=http://flaresolverr:8191/v1
    - ENABLE_SCRAPPEY=True
    - SCRAPPEY_API_KEY=YOUR_API_KEY
    - HTTP_PROXY=http://user@password:proxy:3128
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

| Solver | Environment variable | Description | Values |
| --- | --- | --- | --- |
| DirectHTTP | ENABLE_DIRECTHTTP | Enable DirectHTTP solver | True/False |
| FlareSolverr | ENABLE_FLARESOLVERR | Enable FlareSolverr solver | True/False |
| FlareSolverr | FLARESOLVERR_URL | FlareSolverr API URL. **REQUIRED** if Flasolverr is enabled. | |
| Scrappey | ENABLE_SCRAPPEY | Enable Scrappey solver | True/False |
| Scrappey | SCRAPPEY_API_KEY | Scrappey API key. **REQUIRED** if Scrappey is enabled. |  |

## Configure Prowlarr

Configure this service as a FlareSolverr service in Prowlarr.