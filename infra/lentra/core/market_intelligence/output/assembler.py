from typing import Any, Dict

from lentra.core.market_intelligence.output.contract import (
    MarketIntelligenceOutputContract,
    UIBlock,
    APIBlock,
)


class MarketIntelligenceOutputAssembler:
    """
    Собирает финальный UI/API контракт из сырого результата engine.
    """

    def assemble(self, raw: Dict[str, Any]) -> MarketIntelligenceOutputContract:

        ui = UIBlock(
            price=raw.get("price"),
            market_price=raw.get("market_price"),
            deviation_pct=raw.get("deviation_pct"),
            risk_level=raw.get("risk", {}).get("level"),
            duplicates=raw.get("duplicates", 0),
            verdict=raw.get("verdict", "unknown"),
        )

        api = APIBlock(
            normalized=raw.get("normalized", {}),
            signals=raw.get("signals", {}),
            scores=raw.get("scores", {}),
        )

        return MarketIntelligenceOutputContract(
            ui=ui,
            api=api,
            trace_id=raw.get("trace_id"),
            source_count=raw.get("source_count", 0),
            confidence=raw.get("confidence", 0.0),
        )
