import math

class UnifiedScoreEngine:

    def compute(self, listing: dict):

        price = float(listing.get("price") or 0)
        risk = float(listing.get("risk") or 0.5)
        area = float(listing.get("area_quality") or 5)

        # -------------------------
        # MARKET GAP (SYMMETRIC)
        # -------------------------
        market_price = 500.0
        gap = (price - market_price) / market_price

        price_signal = -gap  # symmetric

        # -------------------------
        # AREA SIGNAL (STABLE SCALE)
        # -------------------------
        area_signal = (area - 5) / 5

        # -------------------------
        # RISK SIGNAL
        # -------------------------
        risk_signal = (0.5 - risk)

        # -------------------------
        # SCORE
        # -------------------------
        score = (
            price_signal * 0.5 +
            area_signal * 0.35 +
            risk_signal * 0.15
        )

        # -------------------------
        # DECISION (STRICTER BOUNDARIES)
        # -------------------------
        if score > 0.3:
            verdict = "fair"
        elif score < -0.3:
            verdict = "overpriced"
        else:
            verdict = "neutral"

        # -------------------------
        # CONFIDENCE (SEPARATE MODEL)
        # NOT DERIVED FROM SCORE SIGN
        # -------------------------
        confidence = (
            0.4 * area_signal +
            0.4 * (1 - risk) +
            0.2 * (1 - abs(gap))
        )

        confidence = max(0.0, min(1.0, confidence))

        listing["final_score"] = score
        listing["verdict"] = verdict
        listing["confidence"] = confidence

        return listing
