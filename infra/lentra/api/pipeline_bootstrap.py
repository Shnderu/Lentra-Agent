from lentra.core.graph_v2.engines.registry import EngineRegistry
from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine


class Orchestrator:
    def __init__(self, registry, mi_engine):
        self.registry = registry
        self.mi_engine = mi_engine

    def execute(self, request):
        """
        Safe execution flow:
        1. Try resolve engine by type if provided
        2. If missing or unknown -> fallback to MarketIntelligenceEngine
        """

        engine_type = request.get("type")

        # если тип явно не задан — сразу MI engine
        if not engine_type:
            return self.mi_engine.execute(request)

        # попытка резолва через registry
        try:
            engine = self.registry.resolve(engine_type)
        except Exception:
            engine = None

        # если engine найден — используем его
        if engine:
            return engine.execute(request)

        # fallback на Market Intelligence layer
        return self.mi_engine.execute(request)


def build_orchestrator():
    registry = EngineRegistry()
    mi_engine = MarketIntelligenceEngine()

    return Orchestrator(registry=registry, mi_engine=mi_engine)
