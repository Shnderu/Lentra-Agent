# ============================================================
# TENANCY SERVICE V16.9
# ============================================================


class TenantService:
    def __init__(self):
        self.tenants = {}

    def create_tenant(self, tenant_id: str, plan="free"):
        self.tenants[tenant_id] = {
            "tenant_id": tenant_id,
            "plan": plan,
            "limits": self._default_limits(plan),
        }

        return self.tenants[tenant_id]

    def _default_limits(self, plan):
        if plan == "enterprise":
            return {"requests_per_min": 10000}

        if plan == "pro":
            return {"requests_per_min": 1000}

        return {"requests_per_min": 100}
