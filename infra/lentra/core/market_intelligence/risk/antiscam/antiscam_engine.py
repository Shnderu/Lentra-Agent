

class AntiScamEngine:

    def score(self, listing: dict, cluster: dict):

        score = 0.0
        signals = []

        price = listing.get("price", 0)
        market = cluster.get("market_price", price)

        # 1. price anomaly
        if market and price:
            deviation = abs(price - market) / max(market, 1)

            if deviation > 0.5:
                score += 0.4
                signals.append("extreme_price_deviation")

            elif deviation > 0.25:
                score += 0.2
                signals.append("price_anomaly")

        # 2. source repetition risk
        sources = cluster.get("sources", [])
        if len(set(sources)) == 1 and len(sources) > 1:
            score += 0.2
            signals.append("single_source_cluster")

        # 3. listing inconsistency
        title = listing.get("title", "")
        if "luxury" in title.lower() and price < 500:
            score += 0.3
            signals.append("luxury_price_mismatch")

        # 4. geo inconsistency
        if listing.get("location") and "beach" in title.lower():
            if "beach" not in listing.get("location", "").lower():
                score += 0.2
                signals.append("geo_mismatch")

        # clamp
        score = min(score, 1.0)

        return {
            "scam_score": round(score, 3),
            "risk_level": self._risk_level(score),
            "signals": signals
        }


    def _risk_level(self, score):

        if score > 0.7:
            return "high_risk"
        elif score > 0.4:
            return "medium_risk"
        else:
            return "low_risk"
