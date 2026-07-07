from lentra.core.market_intelligence.risk.risk_calibration_v1 import RiskCalibrationV1


class RiskEngine:
    """
    Deterministic risk engine with calibration loop.
    """

    def __init__(self):
        self.calibration = RiskCalibrationV1()

    def score(self, entity_id: str, signals: dict) -> float:
        if signals is None:
            signals = {}

        base = self._base_score(signals)

        return self.calibration.calibrated_risk(entity_id, base)

    def _base_score(self, signals: dict) -> float:
        # deterministic scoring rules
        score = 0.5

        if signals.get("duplicates", 0) > 3:
            score += 0.2

        if signals.get("age_days", 0) > 365:
            score += 0.1

        if signals.get("price_anomaly", False):
            score += 0.2

        return max(0.0, min(1.0, score))
