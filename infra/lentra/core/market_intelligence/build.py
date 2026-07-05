from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway


def build_intelligence_gateway():
    """
    SAFE BUILD MODE

    IMPORTANT:
    - SignalsEngineV1 DISABLED
    - pipeline uses direct engines only
    """

    engines = {
        "price_check": object(),
        "risk_score": object(),
        "dedupe": object(),
        "decision_policy": object(),
        "area_v2": object(),
        "expat": object(),
    }

    graph = {
        "nodes": [],
        "edges": []
    }

    return IntelligenceGateway(
        engines=engines,
        graph=graph
    )
