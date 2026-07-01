from lentra.core.market_intelligence.output.assembler import OutputAssembler
from lentra.core.market_intelligence.output.contract import MarketIntelligenceOutputContract


class MarketIntelligenceOutputFacade:

    def __init__(self):
        self.assembler = OutputAssembler()

    def analyze(self, context: dict) -> MarketIntelligenceOutputContract:
        assembled = self.assembler.build(context)

        return MarketIntelligenceOutputContract(
            ui=assembled.get("ui", {}),
            api=assembled.get("api", {}),
            meta=assembled.get("meta", {})
        )
