from lentra.core.market_intelligence.engines import build_engines
from lentra.core.market_intelligence.isolation.engine_registry_v3 import build_registry_v3
from lentra.core.market_intelligence.graph.intelligence_graph import IntelligenceGraph


def build_gateway():
    engines = build_engines()

    registry = build_registry_v3(engines)

    graph = IntelligenceGraph()

    gateway = {
        "registry": registry,
        "graph": graph,
        "handle": lambda payload: registry.evaluate(payload)
    }

    return gateway
