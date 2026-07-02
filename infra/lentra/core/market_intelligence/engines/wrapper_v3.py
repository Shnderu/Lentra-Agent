from lentra.core.market_intelligence.context.engine_context_v3 import EngineContextV3


class EngineWrapperV3:
    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, ctx: EngineContextV3):
        if ctx is None:
            raise RuntimeError("CTX IS NONE")

        if not hasattr(self.engine, "evaluate"):
            raise RuntimeError("ENGINE HAS NO EVALUATE")

        return self.engine.evaluate(ctx)
