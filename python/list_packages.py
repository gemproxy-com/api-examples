"""List the plans on sale (public endpoint, no token needed)."""

from gemproxy import call

for plan in call("/api/public/packages/list", token=""):
    print(f"{plan['code']:<28} {plan['proxyType']:<7} {plan['name']}")
