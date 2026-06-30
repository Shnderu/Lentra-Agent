from typing import Optional

# SAFE IMPORT: no gateway import at module level
# FIX: break circular dependency by lazy import only inside function

def build_intelligence_gateway(orchestrator: Optional[object] = None):
    """
    BOOTSTRAP SAFE FACTORY

    Critical fix:
    - gateway import is LAZY
    - prevents circular import with bootstrap/orchestrator
    """

    # lazy import (break cycle)
    from lentra.core.market_intelligence.gateway import IntelligenceGateway

    gateway = IntelligenceGateway(orchestrator=orchestrator)
    return gateway
