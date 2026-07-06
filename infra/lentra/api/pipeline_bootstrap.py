from lentra.core.graph_v2.engines.registry import EngineRegistry
from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine


class Orchestrator:
    def __init__(self, registry, mi_engine):
        self.registry = registry
        self.mi_engine = mi_engine

    def execute(self, request):
        engine_name = request.get("type")

        # SAFE DEFAULT (фикс падения market_intelligence)
        if not engine_name:
            return self.mi_engine.execute(request)

        try:
            engine = self.registry.resolve(engine_name)
        except KeyError:
            return self.mi_engine.execute(request)

        # ADAPTER LAYER (КРИТИЧЕСКИЙ ФИКС)
        if hasattr(engine, "run") and not hasattr(engine, "execute"):
            return engine.run(request)

        if hasattr(engine, "execute"):
            return engine.execute(request)

        raise RuntimeError(f"Engine {engine_name} has no run/execute method")


def build_orchestrator():
    registry = EngineRegistry()
    mi_engine = MarketIntelligenceEngine()

    return Orchestrator(registry=registry, mi_engine=mi_engine)
