class UnifiedScoringEngine:

    def compute(self, listing: dict) -> dict:

        def safe(v, default=0.5):
            if v is None:
                return default
            try:
                return float(v)
            except Exception:
                return default

        price = safe(listing.get("price"), 0.0)
        market_avg = safe(listing.get("market_avg"), price)
        risk = safe(listing.get("risk"), 0.5)
        area = listing.get("area", {}).get("area_quality", 5)

        # PRICE SIGNAL
        price_signal = 1 - abs(price - market_avg) / max(market_avg, 1)
        price_signal = max(0.0, min(1.0, price_signal))

        # AREA BOOST
        area_signal = (area - 5) * 0.05

        # FINAL SCORE
        score = (price_signal * 0.5) + (area_signal * 0.2) - (risk * 0.3)

        score = max(0.0, min(1.0, score))

        # VERDICT
        if score >= 0.75:
            verdict = "strong_buy"
        elif score >= 0.6:
            verdict = "good_deal"
        elif score >= 0.4:
            verdict = "neutral"
        elif score >= 0.25:
            verdict = "overpriced"
        else:
            verdict = "avoid"

        # CONFIDENCE (простая стабилизация)
        confidence = max(0.1, min(1.0, score + (1 - risk) * 0.2))

        listing["score"] = round(score, 3)
        listing["verdict"] = verdict
        listing["confidence"] = round(confidence, 3)

        return listing
