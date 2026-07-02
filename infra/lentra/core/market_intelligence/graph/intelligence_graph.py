from typing import Dict, Any


class IntelligenceGraph:
    """
    OS-level orchestration graph (safe layer)

    НЕ заменяет gateway.
    Работает как optional enhancer.
    """

    def __init__(self):
        self.nodes = []

    def register(self, name: str, engine):
        self.nodes.append((name, engine))

    def execute(self, payload: Dict[str, Any], engines: Dict[str, Any]) -> Dict[str, Any]:
        """
        SAFE EXECUTION:
        - sequential enrichment
        - no control over gateway logic
        - fallback-safe
        """

        context = {}

        for name, engine in engines.items():
            try:
                result = engine.evaluate(payload)
                context[name] = result
            except Exception as e:
                # CRITICAL: graph must never break system
                context[name] = {
                    "error": str(e),
                    "score": 0.0
                }

        return {
            "graph": context
        }
