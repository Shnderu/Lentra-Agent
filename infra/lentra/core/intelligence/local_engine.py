class LocalEngine:
    """
    Minimal fallback intelligence.
    Не бизнес-логика, только стабильность runtime.
    """

    def interpret(self, query: str, context=None):
        return {
            "result": {
                "query": query,
                "decision": "noop",
            },
            "signals": {},
            "confidence": 0.0,
            "meta": {
                "engine": "local_fallback"
            }
        }
