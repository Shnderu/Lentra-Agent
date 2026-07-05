from lentra.core.graph_v2.engines.registry import EngineRegistry
from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine


class Orchestrator:
    def __init__(self, registry, mi_engine):
        self.registry = registry
        self.mi_engine = mi_engine

    def execute(self, request):
        engine = self.registry.resolve(request.get("type", "market_intelligence"))

        if engine:
            return engine.execute(request)

        return self.mi_engine.execute(request)


def build_orchestrator():
    registry = EngineRegistry()
    mi_engine = MarketIntelligenceEngine()

    return Orchestrator(registry=registry, mi_engine=mi_engine)
