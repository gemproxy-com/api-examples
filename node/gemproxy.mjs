// Small GemProxy API client for Node.js 18+ (built-in fetch).
//
// Every endpoint answers with the same envelope:
//   { "success": true,  "data": ... }
//   { "success": false, "error": "PROXY_ROTATE_COOLDOWN_NOT_REACHED", "message": "...", "code": 40020063 }
// call() returns `data` or throws a GemProxyError carrying the `error` name.

import { existsSync, readFileSync } from 'node:fs';

// Read KEY=value lines from ../.env (existing environment variables win).
const envFile = new URL('../.env', import.meta.url);
if (existsSync(envFile)) {
  for (const line of readFileSync(envFile, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^['"]|['"]$/g, '');
  }
}

export const API = (process.env.GEMPROXY_API || 'https://api.gemproxy.com').replace(/\/$/, '');
export const USER_AGENT = 'gemproxy-api-examples/1.0';

export class GemProxyError extends Error {
  constructor(status, error, message) {
    super(`HTTP ${status} ${error}: ${message}`);
    this.status = status;
    this.error = error;
  }
}

export async function call(path, body = {}, { token = process.env.GEMPROXY_TOKEN, method = 'POST' } = {}) {
  const headers = { 'Content-Type': 'application/json', Accept: 'application/json', 'User-Agent': USER_AGENT };
  if (token) headers['X-Api-Token'] = token;
  const res = await fetch(API + path, {
    method,
    headers,
    body: method === 'GET' ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(30_000),
  });
  let payload;
  try {
    payload = await res.json();
  } catch {
    throw new GemProxyError(res.status, 'HTTP_ERROR', res.statusText);
  }
  if (!payload.success) throw new GemProxyError(res.status, payload.error ?? 'UNKNOWN', payload.message ?? '');
  return payload.data;
}

export function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    console.error(`Missing ${name}: set it in .env or the environment`);
    process.exit(1);
  }
  return value;
}

// Turn the API's "host:port:user:pass" into "scheme://user:pass@host:port".
export function proxyUrl(proxy, scheme = 'http') {
  const [host, port, user, ...rest] = proxy.split(':');
  const e = encodeURIComponent;
  return `${scheme}://${e(user)}:${e(rest.join(':'))}@${host}:${port}`;
}
