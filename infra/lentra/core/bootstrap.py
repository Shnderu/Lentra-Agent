"""
BOOTSTRAP ENTRYPOINT (CLEAN)

RULE:
- ONLY ONE graph build path
- NO indirect orchestrator creation
"""

from lentra.core.market_intelligence.build import build_intelligence_gateway
from lentra.core.intelligence.orchestrator import Orchestrator


def bootstrap():
    orchestrator = Orchestrator()

    gateway = build_intelligence_gateway(orchestrator=orchestrator)

    return gateway


if __name__ == "__main__":
    app = bootstrap()
    print("[BOOTSTRAP] Intelligence Graph OS initialized safely")
