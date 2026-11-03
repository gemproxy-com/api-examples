"""Fetch the key's current proxy and send a request through it.

    python use_proxy.py [key]   # key defaults to GEMPROXY_KEY

urllib speaks HTTP proxies only. For SOCKS5 use `requests[socks]`:
    requests.get(url, proxies={"https": proxy_url(p["socks5"], "socks5h")})
"""

import json
import sys
import urllib.request

from gemproxy import USER_AGENT, call, proxy_url, require

key = sys.argv[1] if len(sys.argv) > 1 else require("GEMPROXY_KEY")
require("GEMPROXY_TOKEN")

current = call("/api/v1/rotate-proxies/get-current-proxy", {"keyValue": key})
url = proxy_url(current["http"])
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": url, "https": url}))
opener.addheaders = [("User-Agent", USER_AGENT)]

with opener.open("https://api.ipify.org?format=json", timeout=30) as res:
    print("Exit IP through the proxy:", json.load(res)["ip"])
