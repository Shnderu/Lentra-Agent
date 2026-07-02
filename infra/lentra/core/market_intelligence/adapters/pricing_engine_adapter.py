from lentra.core.contracts.engine_result import EngineResult


class PricingEngineAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload: dict, context: dict = None) -> dict:
        context = context or {}

        raw = self.engine.evaluate(payload, context)

        deviation = raw.get("deviation_pct", 0.0)

        signal = self._signal(deviation)

        return EngineResult(
            score=self._score(deviation),
            deviation=deviation,
            signal=signal,
            raw=raw
        ).to_dict()

    def _signal(self, deviation: float) -> str:
        if deviation > 20:
            return "risk"
        if deviation > 10:
            return "hold"
        return "buy"

    def _score(self, deviation: float) -> float:
        return min(deviation / 30.0, 1.0)
