class PriceEngine:
    def analyze(self, intent: dict, market: dict = None) -> dict:
        market = market or {}

        price_band = market.get("price_band", {"min": 200, "max": 500})
        avg_price = (price_band["min"] + price_band["max"]) / 2

        budget = intent.get("budget_max") or 0

        deviation = 0
        if budget:
            deviation = ((avg_price - budget) / budget) * 100

        return {
            "avg_price": round(avg_price, 2),
            "status": "fair",
            "deviation_pct": round(deviation, 2)
        }


# stable singleton (IMPORTANT FOR OLD IMPORTS)
price_engine = PriceEngine()
