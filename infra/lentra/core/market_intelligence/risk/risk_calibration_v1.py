from dataclasses import dataclass
from typing import Dict, List
import time


@dataclass
class RiskEvent:
    entity_id: str
    predicted_risk: float
    actual_outcome: float  # 0 = safe, 1 = scam / issue
    timestamp: float


class RiskCalibrationV1:
    """
    Deterministic risk calibration engine.

    No ML.
    Only ratio-based correction.
    """

    def __init__(self):
        self.events: List[RiskEvent] = []

    def log_event(self, entity_id: str, predicted_risk: float, actual_outcome: float):
        self.events.append(
            RiskEvent(
                entity_id=entity_id,
                predicted_risk=predicted_risk,
                actual_outcome=actual_outcome,
                timestamp=time.time(),
            )
        )

    def calibration_factor(self, entity_id: str) -> float:
        relevant = [e for e in self.events if e.entity_id == entity_id]

        if not relevant:
            return 1.0

        avg_pred = sum(e.predicted_risk for e in relevant) / len(relevant)
        avg_actual = sum(e.actual_outcome for e in relevant) / len(relevant)

        if avg_pred == 0:
            return 1.0

        # deterministic correction factor
        return avg_actual / avg_pred

    def calibrated_risk(self, entity_id: str, base_risk: float) -> float:
        factor = self.calibration_factor(entity_id)
        return max(0.0, min(1.0, base_risk * factor))
