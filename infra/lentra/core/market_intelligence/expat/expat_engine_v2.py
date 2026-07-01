from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine

class ExpatEngineV2:
    def __init__(self):
        self._engine = ExpatScoreEngine()

    def process(self, payload: dict):
        # unified contract wrapper
        score = self._engine.score(payload)
        return {
            "internet_score": score,
            "area_score": 0.0,
            "noise_score": 0.0
        }
