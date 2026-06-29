class MarketCardBuilder:
    """
    Final product layer: transforms internal listing into UI-ready card.
    """

    def build(self, listing: dict):

        price = listing.get("price")
        risk = listing.get("risk") or 0.5
        confidence = listing.get("confidence") or 0.5
        verdict = listing.get("verdict") or "neutral"
        explanation = listing.get("explanation") or ""

        segment = listing.get("segment") or "unknown"
        micro = listing.get("micro_market") or "unknown"

        # -------------------------
        # DERIVED METRICS
        # -------------------------
        market_price = listing.get("market_price") or price
        deviation = listing.get("market_deviation") or 0.0

        # -------------------------
        # UI STRUCTURE
        # -------------------------
        card = {
            "price": price,
            "market_price": market_price,
            "deviation": round(deviation * 100, 2),
            "risk": round(risk, 3),
            "confidence": round(confidence, 3),
            "verdict": verdict,

            "location": {
                "segment": segment,
                "micro_market": micro
            },

            "insight": explanation,

            "labels": self._labels(verdict, risk, confidence)
        }

        return card

    def _labels(self, verdict, risk, confidence):

        labels = []

        if verdict == "overpriced":
            labels.append("above_market")
        elif verdict == "cheap":
            labels.append("below_market")
        else:
            labels.append("market_fair")

        if risk > 0.75:
            labels.append("high_risk")
        elif risk < 0.3:
            labels.append("low_risk")

        if confidence < 0.3:
            labels.append("low_confidence")

        return labels
