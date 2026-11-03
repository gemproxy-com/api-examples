// List the plans on sale (public endpoint, no token needed).
import { call } from './gemproxy.mjs';

for (const plan of await call('/api/public/packages/list', {}, { token: '' })) {
  console.log(plan.code.padEnd(28), plan.proxyType.padEnd(7), plan.name);
}
