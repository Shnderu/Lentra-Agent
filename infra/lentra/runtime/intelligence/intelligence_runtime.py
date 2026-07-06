from lentra.runtime.intelligence.intelligence_enforcer import IntelligenceEnforcer


class IntelligenceRuntime:

    def __init__(self):
        self.core = MarketIntelligenceAPI()
        self.enforcer = IntelligenceEnforcer()

    def price(self, data):
        return self.enforcer.validate(
            self.core.calculate_price(data)
        )

    def risk(self, data):
        return self.enforcer.validate(
            self.core.calculate_risk(data)
        )
