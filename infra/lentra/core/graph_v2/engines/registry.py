from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine

class GraphEngineRegistry:
    """
    SAFE proxy registry (NOT new core)
    """

    def __init__(self):
        self.pricing = PricingEngine()

    def run_pricing(self, payload):
        return self.pricing.evaluate(payload=payload)
