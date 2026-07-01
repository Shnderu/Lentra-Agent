from typing import Dict, Any

from lentra.core.market_intelligence.output.assembler import OutputAssembler


class MarketIntelligenceOutputFacadeGuarded:
    """
    STRICT OUTPUT LAYER

    IMPORTANT RULE:
    - NO imports from decision layer
    - NO imports from engine
    """

    def __init__(self):
        self.assembler = OutputAssembler()

    def analyze(self, context: Dict[str, Any]):
        return self.assembler.build(context)
