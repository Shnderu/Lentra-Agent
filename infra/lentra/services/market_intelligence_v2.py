class MarketIntelligenceV2:

    def analyze(self, intent):
        q = (intent.get("query") or "").lower()

        return {
            "location": intent.get("location") or "da nang",
            "signals": {
                "beach": "beach" in q,
                "cheap": "cheap" in q
            },
            "price_band": {
                "min": 200,
                "max": 500
            },
            "mode": "v2"
        }

    def price_check(self, intent, market):
        return {
            "avg_price": 350.0,
            "status": "fair",
            "deviation_pct": -25.0
        }

    def risk_score(self, intent, market):
        return {
            "risk_score": 0.4,
            "risk_level": "low"
        }

    def deduplicate(self, intent, market):
        return {
            "cluster_id": "da_nang_v2_cluster",
            "confidence": 0.65
        }

    def verdict(self, price, risk):
        if risk["risk_score"] > 0.7:
            return "high_risk"
        return "market_ok"
