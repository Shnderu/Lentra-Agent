from lentra.core.market_intelligence.build import build_intelligence_gateway
from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway


def bootstrap_intelligence_system():
    try:
        gateway = build_intelligence_gateway()
    except Exception:
        # Safe boot
        gateway = IntelligenceGateway()

    return {
        "gateway": gateway
    }
