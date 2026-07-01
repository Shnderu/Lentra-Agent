from lentra.core.market_intelligence.output.contract import (
    MarketIntelligenceOutputContract,
    MarketIntelligenceUIBlock,
    MarketIntelligenceAPIBlock,
    MarketIntelligenceMeta,
)


class MarketIntelligenceOutputAssembler:

    def assemble(self, engine_result: dict) -> MarketIntelligenceOutputContract:

        ui = MarketIntelligenceUIBlock(
            price=engine_result.get("price", 0),
            market_price=engine_result.get("market_price", 0),
            deviation_pct=engine_result.get("deviation_pct", 0),
            risk_level=engine_result.get("risk_level", "unknown"),
            duplicates=engine_result.get("duplicates", 0),
            verdict=engine_result.get("verdict", "unknown"),

            area=engine_result.get("area"),
            explanation=engine_result.get("explanation"),
        )

        api = MarketIntelligenceAPIBlock(
            normalized=engine_result.get("normalized", {}),
            signals=engine_result.get("signals", {}),
            scores=engine_result.get("scores", {}),
            dynamics=engine_result.get("dynamics"),
        )

        meta = MarketIntelligenceMeta(
            trace_id=engine_result.get("trace_id", "unknown"),
            source_count=engine_result.get("source_count", 0),
            confidence=engine_result.get("confidence", 0.0),
            confidence_breakdown=engine_result.get("confidence_breakdown"),
        )

        return MarketIntelligenceOutputContract(
            ui=ui.__dict__,
            api=api.__dict__,
            meta=meta.__dict__,
        )
