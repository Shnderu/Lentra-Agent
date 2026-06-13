# ============================================================
# TENANCY MODEL V16.9
# ============================================================

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Tenant:
    tenant_id: str
    plan: str  # free / pro / enterprise
    limits: Dict[str, Any]
