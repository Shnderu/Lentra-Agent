from lentra.core.market_intelligence.output.assembler import OutputAssembler
from lentra.core.market_intelligence.output.contract import MarketIntelligenceOutputContract


class MarketIntelligenceOutputFacadeGuarded:

    def __init__(self):
        self.assembler = OutputAssembler()

    def analyze(self, context: dict) -> MarketIntelligenceOutputContract:
        raw = self.assembler.build(context)

        # HARD ENFORCE CONTRACT (CRITICAL FIX)
        if isinstance(raw, MarketIntelligenceOutputContract):
            return raw

        return MarketIntelligenceOutputContract(
            ui=raw.get("ui", {}),
            api=raw.get("api", {}),
            meta=raw.get("meta", {})
        )
