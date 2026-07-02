from lentra.core.market_intelligence.signal.signal_layer import SignalLayer


class IntelligenceGateway:

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.signal_layer = SignalLayer()

    def evaluate(self, engines: dict, payload: dict) -> dict:

        pricing = engines["pricing"].evaluate(payload)
        risk = engines["risk"].evaluate(payload)
        dedup = engines["dedup"].evaluate(payload)

        signal = self.signal_layer.resolve(pricing, risk, dedup)

        return {
            "signal": signal.value,
            "pricing": pricing,
            "risk": risk,
            "dedup": dedup
        }
