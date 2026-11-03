"""Rotate a key N times, check the exit IP after each rotation, and respect the cooldown.

    python rotate_loop.py [times] [key]    # times defaults to 3, key to GEMPROXY_KEY
"""

import json
import sys
import time
import urllib.request

from gemproxy import USER_AGENT, GemProxyError, call, proxy_url, require

times = int(sys.argv[1]) if len(sys.argv) > 1 else 3
key = sys.argv[2] if len(sys.argv) > 2 else require("GEMPROXY_KEY")
require("GEMPROXY_TOKEN")


def exit_ip(proxy):
    url = proxy_url(proxy)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": url, "https": url}))
    opener.addheaders = [("User-Agent", USER_AGENT)]
    with opener.open("https://api.ipify.org?format=json", timeout=30) as res:
        return json.load(res)["ip"]


done = 0
while done < times:
    try:
        proxy = call("/api/v1/rotate-proxies/rotate", {"keyValue": key})
    except GemProxyError as err:
        if err.error == "PROXY_ROTATE_COOLDOWN_NOT_REACHED":
            print("Cooldown not over yet, retrying in 5 s")
            time.sleep(5)
            continue
        raise SystemExit(str(err))
    done += 1
    print(f"#{done} exit IP {exit_ip(proxy['http'])}")
    if done < times:
        time.sleep(proxy["ttcSeconds"])
