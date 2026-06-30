class FraudDetectionEngineV1:

    def score(self, listing):

        risk = listing.get("risk", 0.5)

        price = listing.get("price", 0)
        market_price = listing.get("market_price", price)

        # anomaly detection v1
        deviation = abs(price - market_price) / max(market_price, 1)

        fraud_score = min(1.0, risk + deviation * 0.5)

        flags = []

        if deviation > 0.3:
            flags.append("price_anomaly")

        if risk > 0.7:
            flags.append("high_base_risk")

        listing["fraud"] = {
            "score": round(fraud_score, 3),
            "flags": flags,
            "status": "suspicious" if fraud_score > 0.7 else "ok"
        }

        return listing
