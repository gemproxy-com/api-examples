# GemProxy API examples

Runnable examples for the [GemProxy](https://gemproxy.com?utm_source=github&utm_medium=bio&utm_campaign=api-examples) API: rotate the IP of a rotating proxy key, read the proxy currently assigned to it, send traffic through it, and list the plans on sale. Each example exists in cURL, Python (standard library only) and Node.js.

GemProxy sells rotating and static proxies with IPs in Vietnam. Full API reference with a Try-it console: [app.gemproxy.com/api-docs](https://app.gemproxy.com/api-docs) (sign-in required).

## Setup

1. Get an API token: dashboard → **API Documentation** → **API Keys** ([open](https://app.gemproxy.com/api-docs#keys)).
2. Have a rotating key you own: dashboard → **Rotating Keys** ([open](https://app.gemproxy.com/rotating-keys)).
3. Copy `.env.example` to `.env` and fill in both values. `.env` is git-ignored; never commit it.

```bash
git clone https://github.com/gemproxy-com/api-examples.git
cd api-examples
cp .env.example .env   # then edit .env
```

## Examples

| Task | cURL | Python 3.8+ | Node.js 18+ |
|---|---|---|---|
| List plans (no token) | [`curl/list-packages.sh`](curl/list-packages.sh) | [`python/list_packages.py`](python/list_packages.py) | [`node/list-packages.mjs`](node/list-packages.mjs) |
| List your active keys | [`curl/list-active-keys.sh`](curl/list-active-keys.sh) | | |
| Current proxy of a key | [`curl/get-current-proxy.sh`](curl/get-current-proxy.sh) | | |
| Rotate a key | [`curl/rotate.sh`](curl/rotate.sh) | [`python/rotate.py`](python/rotate.py) | [`node/rotate.mjs`](node/rotate.mjs) |
| Send a request through the proxy | [`curl/use-proxy.sh`](curl/use-proxy.sh) | [`python/use_proxy.py`](python/use_proxy.py) | [`node/use-proxy.mjs`](node/use-proxy.mjs) |
| Rotate in a loop, respecting the cooldown | | [`python/rotate_loop.py`](python/rotate_loop.py) | |

```bash
# cURL
./curl/rotate.sh
./curl/use-proxy.sh "host:port:user:pass"          # add "socks5" as a second argument for SOCKS5

# Python: no dependencies
cd python && python3 rotate.py && python3 use_proxy.py

# Node.js: use-proxy needs undici
cd node && npm install && node rotate.mjs && node use-proxy.mjs
```

The small clients in [`python/gemproxy.py`](python/gemproxy.py) and [`node/gemproxy.mjs`](node/gemproxy.mjs) are 60 to 80 lines each. Copy them into your own project if they help.

## API basics

**Base URL:** `https://api.gemproxy.com`

**Auth:** send your token in the `X-Api-Token` header. Endpoints under `/api/public/` need no token. The docs also show an `X-Merchant-Id` header; it is optional and GemProxy accounts can leave it out.

**Requests:** `POST` with a JSON body, also when the body is empty (`{}`).

**Responses** share one envelope:

```json
{ "code": 200, "success": true, "status": "SUCCESS", "timestamp": 1730592000000, "data": { } }
{ "code": 40020063, "success": false, "status": "FAIL", "error": "PROXY_ROTATE_COOLDOWN_NOT_REACHED", "message": "Cooldown period not reached for proxy rotation" }
```

Check `success`, then branch on `error`. Business errors such as a cooldown or a low balance come back as HTTP `400`. A request without the `X-Api-Token` header gets `403 ACCESS_DENIED`; a token that is not valid gets `401 UNAUTHORIZED`.

### Rotating proxies

| Endpoint | What it does |
|---|---|
| `POST /api/v1/rotate-proxies/rotate` | New IP for a key. Body: `{"keyValue": "..."}` |
| `POST /api/v1/rotate-proxies/get-current-proxy` | The proxy assigned to a key right now, without rotating |
| `POST /api/v1/rotate-proxies/out` | Release the proxy of one or more keys. Body: `{"keyValues": ["..."]}` |
| `POST /api/v1/keys/find-all-active` | Your keys that are still active |
| `POST /api/public/packages/list` | Plans on sale (public) |

A rotation returns:

```json
{
  "http":   "203.0.113.24:8080:user:pass",
  "socks5": "203.0.113.24:1080:user:pass",
  "ttlSeconds": 1800,
  "ttcSeconds": 60,
  "rotateAvailableAt": 1730592060000
}
```

- `http` and `socks5` use the format `host:port:user:pass`. The password may contain `:`, so split on the first three colons only. Most HTTP clients want `http://user:pass@host:port`, with the user and password URL-encoded; the clients here do that for you.
- `ttcSeconds` is the minimum wait before the next rotation, and `rotateAvailableAt` (epoch milliseconds) is the moment that wait ends. Rotating sooner returns `PROXY_ROTATE_COOLDOWN_NOT_REACHED`.
- `ttlSeconds` is how long the current IP is kept at most.
- The values depend on the plan. The response above uses a documentation IP (203.0.113.0/24).

Errors you are likely to meet:

| `error` | Meaning |
|---|---|
| `ACCESS_DENIED` | No `X-Api-Token` header (HTTP 403) |
| `UNAUTHORIZED` | The token is not valid (HTTP 401) |
| `PROXY_KEY_NOT_FOUND` | No key with that value on your account |
| `PROXY_KEY_EXPIRED` | The key has expired; renew it in the dashboard or with the API |
| `PROXY_KEY_INACTIVE` | The key is turned off |
| `PROXY_ROTATE_COOLDOWN_NOT_REACHED` | Rotated before `ttcSeconds` passed |
| `PROXY_ROTATE_LOCKED` | Rotation is paused for this key after unusual activity |

Static proxies, buying and renewing keys, ISPs and locations have their own endpoints: see the [API docs](https://app.gemproxy.com/api-docs).

## Check before you rely on it

Before you put a proxy to work, check its exit IP and speed: run `use-proxy` from this repo, or open **Proxy Checker** in the [dashboard](https://app.gemproxy.com/proxy-checker). The hourly rotating plan is the cheapest way to try the network. Plans and prices: [gemproxy.com/pricing](https://gemproxy.com/pricing?utm_source=github&utm_medium=bio&utm_campaign=api-examples).

Use the proxies within the law and the terms of the sites you visit. See the [terms of service](https://gemproxy.com/terms-condition?utm_source=github&utm_medium=bio&utm_campaign=api-examples).

## Help

Found a bug in an example? Open an issue in this repo. For your account, keys or payments: [Telegram support](https://t.me/gemproxy_support_bot) or [support@gemproxy.com](mailto:support@gemproxy.com). Never post your token or key in an issue.

## License

The code in this repository is released under the [MIT License](LICENSE). The license covers the code only. The GemProxy name and logo are trademarks and are not licensed for use as your own branding.

---

**Tiếng Việt:** Ví dụ gọi API GemProxy bằng cURL, Python và Node.js: đổi IP cho key xoay, xem proxy hiện tại, gửi request qua proxy, xem danh sách gói. Lấy token ở mục Tài liệu API → API Keys trên dashboard, chép `.env.example` thành `.env` rồi điền token và key. Hỗ trợ: [Telegram](https://t.me/gemproxy_support_bot).
