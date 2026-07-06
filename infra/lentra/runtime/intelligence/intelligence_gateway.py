from lentra.core.market_intelligence.decision.market_decision_core import market_decision_core

class IntelligenceGateway:

    def interpret(self, data: dict):

        decision = market_decision_core(data)

        if decision["score"] > 0.7:
            level = "HIGH_VALUE"
        elif decision["score"] > 0.4:
            level = "MEDIUM_VALUE"
        else:
            level = "LOW_VALUE"

        return {
            "decision": decision,
            "interpretation": level
        }
