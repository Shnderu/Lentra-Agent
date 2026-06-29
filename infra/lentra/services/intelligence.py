from typing import Dict, Any


class MarketIntelligenceService:
    """
    V2 CLEAN CONTRACT:
    ONLY signal extraction.
    NO scoring, NO pricing, NO verdicts.
    """

    def analyze(self, query: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        q = (query or "").lower()

        location = intent.get("location")
        budget = intent.get("budget_max")

        return {
            "location": location or "unknown",
            "budget": budget,
            "signals": {
                "beach": any(x in q for x in ["beach", "sea", "ocean"]),
                "cheap": any(x in q for x in ["cheap", "budget", "low"]),
                "central": any(x in q for x in ["center", "downtown"]),
            }
        }


intelligence_service = MarketIntelligenceService()
