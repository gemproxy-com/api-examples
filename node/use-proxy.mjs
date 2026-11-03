// Fetch the key's current proxy and send a request through it.
//   node use-proxy.mjs [key]    (key defaults to GEMPROXY_KEY)
// Needs `npm install` (undici's ProxyAgent). For SOCKS5, use a SOCKS agent such as `socks-proxy-agent`.
import { ProxyAgent, fetch } from 'undici';
import { USER_AGENT, call, proxyUrl, requireEnv } from './gemproxy.mjs';

const key = process.argv[2] || requireEnv('GEMPROXY_KEY');
requireEnv('GEMPROXY_TOKEN');

const current = await call('/api/v1/rotate-proxies/get-current-proxy', { keyValue: key });
const dispatcher = new ProxyAgent(proxyUrl(current.http));
const res = await fetch('https://api.ipify.org?format=json', { dispatcher, headers: { 'User-Agent': USER_AGENT } });
console.log('Exit IP through the proxy:', (await res.json()).ip);
