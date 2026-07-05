class EngineWrapper:
    """
    Normalizes all engines to single interface.
    """

    def __init__(self, engine):
        self.engine = engine

    def run(self, ctx: dict):
        return self.engine.run(ctx)
