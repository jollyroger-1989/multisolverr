from .flaresolverr import FlareSolverrClient


class ByparrClient(FlareSolverrClient):
    """Byparr (https://github.com/ThePhaseless/Byparr) speaks the same wire
    protocol as FlareSolverr for GET requests, so it reuses that client's
    request/response handling as-is.

    It does not implement request.post, though: its request model has no
    postData or cookies fields at all, and it always performs a plain GET
    navigation regardless of the `cmd` sent ("Type of request, currently
    only supports GET requests", per Byparr's own LinkRequest docstring).
    POST it a login/form submission and it still replies 200 — for a blank,
    freshly re-rendered GET of the page, with the submitted data silently
    discarded.

    Declaring only GET here (instead of inheriting FlareSolverrClient's
    ['GET', 'POST']) means the pipeline loop in multisolverr.py correctly
    skips this step for request.post and falls through to a solver that
    actually supports it, instead of returning that misleading "success".
    """

    def capabilities(self):
        return ['GET']
