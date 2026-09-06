import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import KnowledgeError


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def json_request(url: str, *, headers=None, body=None, timeout=30, attempts=1):
    request = Request(url, data=None if body is None else json.dumps(body).encode(),
                      headers={"Content-Type": "application/json", **(headers or {})})
    opener = build_opener(NoRedirect)
    for attempt in range(attempts):
        try:
            with opener.open(request, timeout=timeout) as response:
                raw = response.read(8_000_001)
                if len(raw) > 8_000_000:
                    raise KnowledgeError("Response exceeded the knowledge connector limit")
                return json.loads(raw)
        except HTTPError as exc:
            if (exc.code == 429 or exc.code >= 500) and attempt + 1 < attempts:
                try:
                    delay = float(exc.headers.get("Retry-After", 2 ** attempt))
                except ValueError:
                    delay = 2 ** attempt
                time.sleep(min(30, max(0, delay)))
                continue
            raise KnowledgeError(f"Knowledge dependency returned HTTP {exc.code}") from None
        except (URLError, TimeoutError, OSError, ValueError):
            if attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            raise KnowledgeError(
                "Knowledge dependency is unreachable or returned invalid JSON"
            ) from None
