from lentra.core.market_intelligence.engines.engine_adapter import EngineAdapter

class EngineRegistryV2:

    def __init__(self, engines: dict):
        self.engines = {
            name: EngineAdapter(engine)
            for name, engine in engines.items()
        }

    def evaluate_all(self, ctx):
        return {
            name: engine.evaluate(ctx)
            for name, engine in self.engines.items()
        }
