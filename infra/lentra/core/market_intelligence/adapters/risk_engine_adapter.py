from lentra.core.contracts.engine_result import EngineResult


class RiskEngineAdapter:
    """
    ARCH V2 CLEAN CONTRACT:
    - score: normalized risk
    - deviation: normalized deviation (pct-safe)
    - raw: untouched engine output
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload: dict, context: dict = None) -> dict:
        context = context or {}

        raw = self.engine.process(payload)

        risk_level = raw.get("risk", 0.5)

        # FIX: support both legacy + normalized engines
        deviation = (
            raw.get("deviation")
            or raw.get("deviation_pct")
            or 0.0
        )

        return EngineResult(
            score=float(risk_level),
            deviation=float(deviation),
            signal=self._signal(risk_level),
            raw=raw
        ).to_dict()

    def _signal(self, score: float) -> str:
        if score >= 0.7:
            return "risk"
        if score >= 0.4:
            return "hold"
        return "buy"
