from typing import Any, Dict

from lentra.core.market_intelligence.output.assembler import MarketIntelligenceOutputAssembler


class MarketIntelligenceEngine:
    """
    CORE ENGINE (PURE)

    НЕ ЗНАЕТ ПРО FACADE
    """

    def __init__(self):
        self.assembler = MarketIntelligenceOutputAssembler()

    def analyze(self, payload: Dict[str, Any]):
        # MOCK / CORE PIPELINE RESULT (временно)
        raw = {
            "price": payload.get("price"),
            "market_price": 650,
            "deviation_pct": ((payload.get("price", 0) - 650) / 650) * 100,
            "risk": {"level": "medium"},
            "duplicates": 3,
            "verdict": "ok",
            "normalized": payload,
            "signals": {},
            "scores": {},
            "trace_id": "local-test",
            "source_count": 1,
            "confidence": 0.72,
        }

        return self.assembler.assemble(raw)

    def interpret(self, payload: Dict[str, Any]):
        return self.analyze(payload)
