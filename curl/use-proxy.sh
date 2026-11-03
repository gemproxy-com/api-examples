#!/usr/bin/env bash
# Send a request through a proxy and print the exit IP.
# Takes the proxy string the API returns ("host:port:user:pass", the `http` or `socks5` field).
# Usage: ./use-proxy.sh <host:port:user:pass> [http|socks5]
set -euo pipefail
[ $# -ge 1 ] || { echo "Usage: $0 <host:port:user:pass> [http|socks5]" >&2; exit 1; }
IFS=: read -r HOST PORT USER PASS <<< "$1"
MODE="${2:-http}"

if [ "$MODE" = socks5 ]; then
  # socks5h: DNS is resolved by the proxy too
  curl -sS --max-time 30 -x "socks5h://$HOST:$PORT" -U "$USER:$PASS" https://api.ipify.org
else
  curl -sS --max-time 30 -x "http://$HOST:$PORT" -U "$USER:$PASS" https://api.ipify.org
fi
echo
