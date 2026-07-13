from lentra.core.contracts.engine_result import EngineResult


class PricingEngineAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Bridges Market Intelligence PricingEngine
    into unified engine contract.
    """

    def __init__(self, engine):
        self.engine = engine


    def evaluate(
        self,
        payload: dict,
        context: dict = None
    ) -> dict:

        context = context or {}

        raw = self.engine.evaluate(
            payload,
            context
        )


        pricing = raw.get(
            "pricing",
            {}
        )


        deviation = float(
            pricing.get(
                "deviation",
                0.0
            )
        )


        score = float(
            pricing.get(
                "score",
                0.5
            )
        )


        signal = self._signal(
            deviation
        )


        return EngineResult(
            score=score,
            deviation=deviation,
            signal=signal,
            raw=raw
        ).to_dict()


    def _signal(
        self,
        deviation: float
    ) -> str:

        deviation_abs = abs(
            deviation
        )


        if deviation_abs > 0.20:
            return "risk"

        if deviation_abs > 0.10:
            return "hold"

        return "buy"
