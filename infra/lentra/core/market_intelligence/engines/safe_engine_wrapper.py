class SafeEngineWrapper:
    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload, result=None):
        """
        Unified ABI:
        - accepts (payload)
        - ignores ctx/result mismatch
        """
        try:
            if hasattr(self.engine, "evaluate"):
                fn = self.engine.evaluate

                # safest possible call
                try:
                    return fn(payload)
                except TypeError:
                    return fn(payload, result or {})

            return {
                "status": "failed",
                "error": "no_evaluate_method"
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
