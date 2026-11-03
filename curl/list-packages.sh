#!/usr/bin/env bash
# List the plans on sale. Public endpoint: no token needed.
. "$(dirname "$0")/_env.sh"

curl -sS -X POST "$GEMPROXY_API/api/public/packages/list" \
  -H "Content-Type: application/json" \
  -H "Accept-Language: en" \
  -d '{}'
echo
