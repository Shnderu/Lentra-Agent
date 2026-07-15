from lentra.core.contracts.engine_result import EngineResult


class RiskEngineAdapter:

    def __init__(self, engine):
        self.engine = engine

    def evaluate(
        self,
        payload: dict,
        market_stats: dict = None,
        duplicate_count: int = 0,
    ) -> dict:

        enriched_payload = {
            **payload,
            "_risk_context": {
                "market_stats": market_stats or {},
                "duplicate_count": duplicate_count,
            },
        }

        result = self.engine.run(enriched_payload)

        risk = result.get("risk", {})

        risk_score = float(risk.get("fraud_score", 0.0))
        risk_level = risk.get("level", "unknown")
        signals = risk.get("signals", [])

        engine_result = EngineResult(
            engine_name="risk_engine",
            data={
                "risk_score": risk_score,
                "risk_level": risk_level,
                "signals": signals,
                "source": risk.get("source", "unknown"),
            },
            trace={
                "adapter": "RiskEngineAdapter",
                "duplicate_count": duplicate_count,
            },
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "signals": signals,
            "engine_result": engine_result.__dict__,
        }
