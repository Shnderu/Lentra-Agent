from lentra.core.market_intelligence.build import build_intelligence_gateway


def bootstrap_intelligence_system():
    try:
        gateway = build_intelligence_gateway()
    except Exception:
        from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway
        gateway = IntelligenceGateway()

    return {
        "gateway": gateway
    }
