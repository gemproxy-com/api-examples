#!/usr/bin/env bash
# List your rotating keys that are still active.
. "$(dirname "$0")/_env.sh"
need GEMPROXY_TOKEN

curl -sS -X POST "$GEMPROXY_API/api/v1/keys/find-all-active" \
  -H "X-Api-Token: $GEMPROXY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
echo
