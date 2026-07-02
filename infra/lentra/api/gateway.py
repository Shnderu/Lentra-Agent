from typing import Dict, Any


class Gateway:
    def __init__(self, pricing_engine):
        self.pricing_engine = pricing_engine

    def handle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.pricing_engine.evaluate(payload)


# SAFE EXPORT
gateway = None
