from lentra.core.market_intelligence.build import build_intelligence_gateway


def get_gateway():
    """
    V2 LOCKED CONTRACT
    - no routing_map
    - no injection config
    - no dynamic wiring
    """

    gateway, engines = build_intelligence_gateway()
    return gateway, engines
