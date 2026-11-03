"""Rotate a key once and print the new proxy.

    python rotate.py [key]      # key defaults to GEMPROXY_KEY
"""

import sys

from gemproxy import GemProxyError, call, require

key = sys.argv[1] if len(sys.argv) > 1 else require("GEMPROXY_KEY")
require("GEMPROXY_TOKEN")

try:
    proxy = call("/api/v1/rotate-proxies/rotate", {"keyValue": key})
except GemProxyError as err:
    if err.error == "PROXY_ROTATE_COOLDOWN_NOT_REACHED":
        raise SystemExit("Too soon: wait for the key's cooldown (ttcSeconds) before rotating again.")
    raise SystemExit(str(err))

print("HTTP:  ", proxy["http"])
print("SOCKS5:", proxy["socks5"])
print(f"Next rotation allowed in {proxy['ttcSeconds']} s; this IP lives up to {proxy['ttlSeconds']} s.")
