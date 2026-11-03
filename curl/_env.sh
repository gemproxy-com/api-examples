# Shared by the scripts in this folder: loads ../.env and sets defaults.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$ROOT/.env" ]; then set -a; . "$ROOT/.env"; set +a; fi
GEMPROXY_API="${GEMPROXY_API:-https://api.gemproxy.com}"
need() { [ -n "${!1:-}" ] || { echo "Missing $1 (set it in .env or the environment)" >&2; exit 1; }; }
