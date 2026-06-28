

class AreaIntelligenceEngine:

    def build(self, listings: list):

        if not listings:
            return {}

        # aggregate signals
        internet = []
        noise = []
        expat = []
        prices = []

        for l in listings:

            area = l.get("location", "")

            # heuristics (placeholder intelligence layer)
            if "wifi" in l.get("title", "").lower():
                internet.append(8)

            if "beach" in area.lower():
                expat.append(8)

            noise.append(5)  # placeholder baseline
            prices.append(l.get("price", 0))

        avg_price = sum(prices) / max(len(prices), 1)

        return {
            "internet_score": sum(internet) / max(len(internet), 1) if internet else 5,
            "noise_score": sum(noise) / len(noise),
            "expat_density": sum(expat) / max(len(expat), 1) if expat else 5,

            "price_index": round(avg_price, 2),

            "area_quality": round(
                (sum(internet) + sum(expat)) / max(len(listings), 1), 2
            ),

            "trend_hint": "stable"
        }
