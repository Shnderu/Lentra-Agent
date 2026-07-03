from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1
from lentra.core.market_intelligence.features.feature_normalizer_v1 import FeatureNormalizerV1


class MarketIntelligenceEngine:

    def __init__(self, config=None):
        self.config = config or {}
        self.signals = SignalsEngineV1()
        self.normalizer = FeatureNormalizerV1()

    # =========================
    # ISOLATOR COMPATIBILITY
    # =========================

    def fetch(self, payload: dict) -> dict:
        return self._compute(payload)

    def normalize(self, data: dict) -> dict:
        return data

    def dedup(self, data: dict) -> dict:
        return data

    def rank(self, data: dict) -> dict:
        return data

    def risk(self, data: dict) -> dict:
        return data

    def build(self, data: dict) -> dict:
        return data

    # =========================
    # CORE LOGIC
    # =========================

    def _compute(self, payload: dict) -> dict:
        signals = self.signals.build(payload)
        features = self.normalizer.normalize(signals, payload)

        risk = signals.get("risk") or {}
        dedup = signals.get("dedup") or {}
        pricing = signals.get("pricing") or {}

        ranking_score = self._safe_ranking(features, risk, pricing)

        return {
            "dedup": {
                "score": dedup.get("score", 1.0),
                "confidence": dedup.get("confidence", 1.0)
            },
            "ranking": {
                "score": float(ranking_score)
            },
            "risk": {
                "risk_level": risk.get("score", 0.0)
            },
            "signals": signals,
            "features": features
        }

    def _safe_ranking(self, features, risk, pricing):
        base = pricing.get("score", 0.5)
        penalty = risk.get("score", 0.0)
        return max(0.0, min(1.0, base * (1.0 - penalty)))
