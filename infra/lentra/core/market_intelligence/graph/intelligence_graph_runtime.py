class IntelligenceGraphRuntime:
    """
    SAFE OS GRAPH v2
    ROLE:
      - normalize engine outputs
      - enrich structure
      - NEVER decide anything
    """

    def build(self, engine_outputs: dict) -> dict:
        return {
            "facts": {
                "price": engine_outputs.get("pricing"),
                "signal": engine_outputs.get("signal"),
                "risk": engine_outputs.get("risk"),
                "dedup": engine_outputs.get("dedup"),
                "expat": engine_outputs.get("expat"),
            },
            "features": {},
            "derived": {},
            "signals": {}
        }
