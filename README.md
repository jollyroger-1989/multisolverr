# MultiSolverr

## Docker compose basic configuration

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

*The HTTP_PROXY config is mandotary*

## Solvers

### DirectHTTP

DirectHTTP is a simple solver that uses the requests library to fetch the page and return the content.

### FlareSolverr

FlareSolverr is a solver that uses the FlareSolverr API to solve Cloudflare challenges.

### Scrappey

Scrappey is a solver that uses the Scrappey API to solve Cloudflare challenges.


## Configure solvers

| Solver | Environment variable | Description |
| --- | --- | --- |
| DirectHTTP | ENABLE_DIRECTHTTP | Enable DirectHTTP solver |
| FlareSolverr | ENABLE_FLARESOLVERR | Enable FlareSolverr solver |
| FlareSolverr | FLARESOLVERR_URL | FlareSolverr API URL. *REQUIRED* if Flasolverr is enabled. |
| Scrappey | ENABLE_SCRAPPEY | Enable Scrappey solver |
| Scrappey | SCRAPPEY_API_KEY | Scrappey API key. *REQUIRED* if Scrappey is enabled. |