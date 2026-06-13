# ============================================================
# RATE LIMIT MIDDLEWARE V16.9
# ============================================================

from lentra.ratelimit.limiter import RateLimiter


class RateLimitMiddleware:
    def __init__(self, tenant_service):
        self.limiter = RateLimiter()
        self.tenants = tenant_service

    def check(self, tenant_id: str):
        tenant = self.tenants.tenants.get(tenant_id)

        if not tenant:
            raise Exception("Tenant not found")

        limit = tenant["limits"]["requests_per_min"]

        if not self.limiter.allow(tenant_id, limit):
            raise Exception("Rate limit exceeded")

        return True
