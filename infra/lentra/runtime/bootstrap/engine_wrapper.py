class EngineWrapper:

    def __init__(self, engine):
        self.engine = engine

    def __call__(self, context: dict):

        # NEW STANDARD
        if hasattr(self.engine, "run") and callable(self.engine.run):
            return self.engine.run(context)

        # LEGACY SUPPORT
        if hasattr(self.engine, "process") and callable(self.engine.process):
            return self.engine.process(context)

        if hasattr(self.engine, "execute") and callable(self.engine.execute):
            return self.engine.execute(context)

        # IF RAW OBJECT → try attribute-based inference
        if hasattr(self.engine, "__dict__"):

            # attempt safe introspection fallback
            return {
                "type": self.engine.__class__.__name__,
                "status": "wrapped_no_op",
                "data": {}
            }

        return {}
