
class EngineAdapterV2:
    """
    UNIVERSAL ENGINE ABI NORMALIZER

    Supports:
    - V1: evaluate(payload)
    - V0: evaluate(payload, result)
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload):
        fn = self.engine.evaluate

        try:
            # V1 engines
            return fn(payload)

        except TypeError:
            # V0 engines (legacy)
            result = {}

            try:
                fn(payload, result)
                return result
            except Exception as e:
                return {
                    "status": "failed",
                    "error": str(e)
                }
