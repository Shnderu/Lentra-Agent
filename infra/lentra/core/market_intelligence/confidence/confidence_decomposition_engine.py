class ConfidenceDecompositionEngine:
    """
    Splits confidence into orthogonal uncertainty components:
    - market uncertainty
    - data uncertainty
    - decision stability
    """

    def compute(self, listing: dict):

        volatility = listing.get("market_volatility") or 0.5
        risk = listing.get("risk") or 0.5
        pressure = listing.get("market_pressure") or 0.0

        # -------------------------
        # 1. MARKET UNCERTAINTY
        # -------------------------
        market_uncertainty = min(1.0, volatility)

        # -------------------------
        # 2. DATA UNCERTAINTY
        # -------------------------
        # proxy: risk + missing structure signals
        photos = listing.get("photos") or []
        missing_data_penalty = 0.2 if len(photos) == 0 else 0.0

        data_uncertainty = min(1.0, risk * 0.6 + missing_data_penalty)

        # -------------------------
        # 3. DECISION UNCERTAINTY
        # -------------------------
        decision_uncertainty = min(1.0, abs(pressure) / 2.0)

        # -------------------------
        # FINAL CONFIDENCE (DECOMPOSED)
        # -------------------------
        total_uncertainty = (
            0.4 * market_uncertainty +
            0.3 * data_uncertainty +
            0.3 * decision_uncertainty
        )

        confidence = 1.0 - total_uncertainty

        # clamp
        confidence = max(0.05, min(1.0, confidence))

        listing["confidence"] = float(confidence)

        listing["confidence_breakdown"] = {
            "market_uncertainty": market_uncertainty,
            "data_uncertainty": data_uncertainty,
            "decision_uncertainty": decision_uncertainty
        }

        return listing
