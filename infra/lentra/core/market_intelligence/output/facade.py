from typing import Any, Dict

from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.market_intelligence.output.assembler import MarketIntelligenceOutputAssembler


class MarketIntelligenceOutputFacade:
    """
    ЕДИНАЯ ТОЧКА ВЫХОДА ИНТЕЛЛЕКТА

    ВСЕ должно проходить через неё:
    - API
    - bot
    - worker
    - runtime
    """

    def __init__(self):
        self.engine = MarketIntelligenceEngine()
        self.assembler = MarketIntelligenceOutputAssembler()

    def analyze(self, payload: Dict[str, Any]):
        raw = self.engine.analyze(payload)
        return self.assembler.assemble(raw)
