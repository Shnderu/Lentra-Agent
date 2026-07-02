from lentra.core.contracts.engine_result import EngineResult


class DedupEngineAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload: dict, context: dict = None) -> dict:
        context = context or {}

        raw = self.engine.evaluate(payload, context)

        matches = raw.get("matches", 0)

        signal = "duplicate" if matches > 1 else "unique"

        return EngineResult(
            score=self._score(matches),
            deviation=0.0,
            signal=signal,
            raw=raw
        ).to_dict()

    def _score(self, matches: int) -> float:
        return min(matches / 5.0, 1.0)
