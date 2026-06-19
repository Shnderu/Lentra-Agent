from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Intent:
    name: str
    confidence: float
    scenario: str
    payload: Dict[str, Any]


class IntentRouterV1:

    def route(self, request: Dict[str, Any]) -> Intent:
        """
        Minimal deterministic router (v1 freeze).
        No ML, no expansion logic.
        """

        text = (request.get("text") or "").lower()

        # -------------------------
        # SIMPLE RULE ROUTING ONLY
        # -------------------------

        if "rent" in text or "apartment" in text:
            return Intent(
                name="rent_search",
                confidence=0.9,
                scenario="rent_scenario_v1",
                payload=request
            )

        if "price" in text or "cost" in text:
            return Intent(
                name="pricing_query",
                confidence=0.8,
                scenario="pricing_scenario_v1",
                payload=request
            )

        # DEFAULT FALLBACK
        return Intent(
            name="unknown",
            confidence=0.3,
            scenario="fallback_scenario_v1",
            payload=request
        )


# singleton
router = IntentRouterV1()
