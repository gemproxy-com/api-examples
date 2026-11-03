#!/usr/bin/env bash
# Ask for a new IP on a rotating key.
# Calling again before `ttcSeconds` has passed returns PROXY_ROTATE_COOLDOWN_NOT_REACHED.
# Usage: ./rotate.sh [key]   (defaults to GEMPROXY_KEY)
. "$(dirname "$0")/_env.sh"
need GEMPROXY_TOKEN
KEY="${1:-${GEMPROXY_KEY:-}}"; [ -n "$KEY" ] || { echo "Pass a key or set GEMPROXY_KEY" >&2; exit 1; }

curl -sS -X POST "$GEMPROXY_API/api/v1/rotate-proxies/rotate" \
  -H "X-Api-Token: $GEMPROXY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"keyValue\":\"$KEY\"}"
echo
