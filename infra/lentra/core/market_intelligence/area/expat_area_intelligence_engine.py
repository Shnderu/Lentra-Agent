from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AreaSignals:
    internet: float = 0.0
    safety: float = 0.0
    noise: float = 0.0
    infrastructure: float = 0.0
    expat_density: float = 0.0
    walkability: float = 0.0
    transport: float = 0.0
    cafes: float = 0.0
    coworking: float = 0.0
    beach_distance: float = 0.0


class ExpatAreaIntelligenceEngine:
    """
    Expat Area Intelligence Engine v1

    Produces normalized area intelligence for downstream
    ranking, concierge and AI decision layers.
    """

    def score(self, signals: AreaSignals) -> Dict[str, Any]:
        internet = self._clamp(signals.internet)
        safety = self._clamp(signals.safety)
        noise = self._clamp(signals.noise)
        infrastructure = self._clamp(signals.infrastructure)
        expat_density = self._clamp(signals.expat_density)
        walkability = self._clamp(signals.walkability)
        transport = self._clamp(signals.transport)
        cafes = self._clamp(signals.cafes)
        coworking = self._clamp(signals.coworking)
        beach_distance = self._clamp(signals.beach_distance)

        overall = (
            internet * 0.18 +
            safety * 0.18 +
            infrastructure * 0.15 +
            expat_density * 0.12 +
            walkability * 0.10 +
            transport * 0.08 +
            cafes * 0.06 +
            coworking * 0.06 +
            beach_distance * 0.04 +
            (10.0 - noise) * 0.03
        )

        overall = round(overall, 2)

        return {
            "overall_score": overall,
            "internet": internet,
            "safety": safety,
            "noise": noise,
            "infrastructure": infrastructure,
            "expat_density": expat_density,
            "walkability": walkability,
            "transport": transport,
            "cafes": cafes,
            "coworking": coworking,
            "beach_distance": beach_distance,
            "classification": self._classify(overall),
        }

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(10.0, float(value)))

    @staticmethod
    def _classify(score: float) -> str:
        if score >= 8.5:
            return "excellent"

        if score >= 7.0:
            return "good"

        if score >= 5.5:
            return "average"

        return "weak"
