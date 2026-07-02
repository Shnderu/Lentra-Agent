class EngineAdapter:
    """
    NORMALIZES ALL ENGINE CONTRACTS TO SINGLE FORMAT
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, ctx, result=None):
        # normalize ctx
        if ctx is None:
            ctx = {}

        # unwrap EngineContext if needed
        if hasattr(ctx, "__dict__"):
            ctx = ctx.__dict__

        # normalize call signatures
        try:
            if result is not None:
                return self.engine.evaluate(ctx, result)
            return self.engine.evaluate(ctx)
        except TypeError:
            # fallback legacy signature
            return self.engine.evaluate(ctx)
