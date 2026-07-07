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
    Only bounded, confidence-weighted correction.
    """

    # Number of events at which we fully trust observed outcomes.
    FULL_CONFIDENCE_EVENTS = 10

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

    def _relevant_events(self, entity_id: str) -> List[RiskEvent]:
        return [e for e in self.events if e.entity_id == entity_id]

    def calibration_factor(self, entity_id: str) -> float:
        """
        Bounded correction factor.

        Returns the ratio of observed outcome to predicted risk,
        clamped to a sane range so a few noisy events cannot cause
        runaway scaling.
        """
        relevant = self._relevant_events(entity_id)

        if not relevant:
            return 1.0

        avg_pred = sum(e.predicted_risk for e in relevant) / len(relevant)
        avg_actual = sum(e.actual_outcome for e in relevant) / len(relevant)

        if avg_pred == 0:
            return 1.0

        factor = avg_actual / avg_pred

        # deterministic clamp to avoid runaway scaling
        return max(0.25, min(4.0, factor))

    def calibrated_risk(self, entity_id: str, base_risk: float) -> float:
        """
        Blend the base risk toward observed outcomes.

        The more events we have for an entity, the more we trust the
        observed average outcome over the raw base risk. This keeps the
        result bounded, deterministic and stable.
        """
        relevant = self._relevant_events(entity_id)

        if not relevant:
            return max(0.0, min(1.0, base_risk))

        avg_actual = sum(e.actual_outcome for e in relevant) / len(relevant)

        confidence = min(1.0, len(relevant) / self.FULL_CONFIDENCE_EVENTS)

        calibrated = (1.0 - confidence) * base_risk + confidence * avg_actual

        return max(0.0, min(1.0, calibrated))
