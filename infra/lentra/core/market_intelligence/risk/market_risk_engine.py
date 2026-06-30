class MarketRiskEngine:

    def score(self, listing: dict):

        score = 0.0

        if listing.get("anomaly_flag"):
            score += 0.4

        if listing.get("price") and listing.get("market_median"):
            deviation = abs(listing["price"] - listing["market_median"]) / listing["market_median"]

            if deviation > 0.3:
                score += 0.3

        listing["market_risk_score"] = min(score, 1.0)

        return listing
