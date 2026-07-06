from lentra.core.market_intelligence.build import build_intelligence_gateway


def init_runtime():
    return {
        "gateway": build_intelligence_gateway()
    }
