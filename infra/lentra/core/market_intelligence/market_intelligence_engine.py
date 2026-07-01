from typing import Any, Dict

from lentra.core.market_intelligence.output.assembler import MarketIntelligenceOutputAssembler


class MarketIntelligenceEngine:
    """
    PURE INTELLIGENCE CORE
    НЕ ЗНАЕТ ПРО FACADE
    """

    def __init__(self):
        self.assembler = MarketIntelligenceOutputAssembler()

    def analyze(self, payload: Dict[str, Any]):
        raw = self._run_pipeline(payload)
        return self.assembler.assemble(raw)

    def interpret(self, payload: Dict[str, Any]):
        return self.analyze(payload)

    def _run_pipeline(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # временная стабилизированная модель (MVP intelligence core)
        price = payload.get("price", 0)
        market_price = 650

        return {
            "price": price,
            "market_price": market_price,
            "deviation_pct": ((price - market_price) / market_price) * 100 if market_price else 0,
            "risk": {"level": "medium"},
            "duplicates": 3,
            "verdict": "ok",
            "normalized": payload,
            "signals": {},
            "scores": {},
            "trace_id": "core-v1",
            "source_count": 1,
            "confidence": 0.72,
        }
