# ============================================================
# RATE LIMITER V16.9
# ============================================================

import time
from collections import defaultdict


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def allow(self, tenant_id: str, limit: int):
        now = time.time()

        window = self.requests[tenant_id]

        # cleanup
        self.requests[tenant_id] = [t for t in window if now - t < 60]

        if len(self.requests[tenant_id]) >= limit:
            return False

        self.requests[tenant_id].append(now)
        return True
