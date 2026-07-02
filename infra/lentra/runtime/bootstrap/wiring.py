from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway
from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine


def build_gateway():
    engines = {
        "pricing": PricingEngine()
    }

    graph = {
        "enabled": True
    }

    return IntelligenceGateway(
        engines=engines,
        graph=graph
    )
