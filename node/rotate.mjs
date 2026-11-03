// Rotate a key once and print the new proxy.
//   node rotate.mjs [key]    (key defaults to GEMPROXY_KEY)
import { GemProxyError, call, requireEnv } from './gemproxy.mjs';

const key = process.argv[2] || requireEnv('GEMPROXY_KEY');
requireEnv('GEMPROXY_TOKEN');

try {
  const proxy = await call('/api/v1/rotate-proxies/rotate', { keyValue: key });
  console.log('HTTP:  ', proxy.http);
  console.log('SOCKS5:', proxy.socks5);
  console.log(`Next rotation allowed in ${proxy.ttcSeconds} s; this IP lives up to ${proxy.ttlSeconds} s.`);
} catch (err) {
  if (err instanceof GemProxyError && err.error === 'PROXY_ROTATE_COOLDOWN_NOT_REACHED') {
    console.error("Too soon: wait for the key's cooldown (ttcSeconds) before rotating again.");
  } else {
    console.error(err.message);
  }
  process.exit(1);
}
