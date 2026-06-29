class MarketIntelligence:
    def analyze(self, intent: dict) -> dict:
        query = (intent.get("query") or "").lower()

        score = 0
        if "beach" in query:
            score += 2
        if "cheap" in query:
            score += 2

        return {
            "price_score": 100 - score * 10,
            "risk": "low" if score > 2 else "medium",
            "market_position": "below_market" if "cheap" in query else "unknown"
        }


market_intelligence = MarketIntelligence()
