from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway


def bootstrap_intelligence_system():
    """
    SAFE BOOTSTRAP v2

    RULES:
    - NO kwargs injection into Gateway
    - NO external engine registry injection
    - SINGLETON safe init
    """

    gateway = IntelligenceGateway()

    return {
        "gateway": gateway
    }
