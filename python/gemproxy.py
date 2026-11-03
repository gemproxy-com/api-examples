"""Small GemProxy API client, standard library only (Python 3.8+).

Every endpoint answers with the same envelope:
    {"success": true,  "data": ...}
    {"success": false, "error": "PROXY_ROTATE_COOLDOWN_NOT_REACHED", "message": "...", "code": 40020063}
`call()` returns `data` or raises GemProxyError with the `error` name.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "gemproxy-api-examples/1.0"


def load_env(path=Path(__file__).resolve().parent.parent / ".env"):
    """Read KEY=value lines from ../.env into os.environ (existing variables win)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
API = os.environ.get("GEMPROXY_API", "https://api.gemproxy.com").rstrip("/")


class GemProxyError(Exception):
    def __init__(self, status, error, message):
        super().__init__(f"HTTP {status} {error}: {message}")
        self.status = status
        self.error = error
        self.message = message


def call(path, body=None, token=None, method="POST", timeout=30):
    """Call an endpoint and return its `data`. `token` defaults to GEMPROXY_TOKEN."""
    token = token if token is not None else os.environ.get("GEMPROXY_TOKEN")
    data = None if method == "GET" else json.dumps(body or {}).encode()
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    if token:
        req.add_header("X-Api-Token", token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            status, payload = res.status, json.load(res)
    except urllib.error.HTTPError as err:
        status = err.code
        try:
            payload = json.load(err)
        except ValueError:
            raise GemProxyError(status, "HTTP_ERROR", err.reason) from None
    if not payload.get("success"):
        raise GemProxyError(status, payload.get("error", "UNKNOWN"), payload.get("message", ""))
    return payload.get("data")


def require(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing {name}: set it in .env or the environment")
    return value


def proxy_url(proxy, scheme="http"):
    """Turn the API's "host:port:user:pass" into "scheme://user:pass@host:port"."""
    host, port, user, password = proxy.split(":", 3)
    q = urllib.parse.quote
    return f"{scheme}://{q(user, safe='')}:{q(password, safe='')}@{host}:{port}"

