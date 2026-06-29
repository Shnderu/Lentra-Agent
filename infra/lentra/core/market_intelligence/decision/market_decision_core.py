from lentra.core.market_intelligence.decision.market_contrast_engine import MarketContrastEngine


class MarketDecisionCore:

    def __init__(self):
        self.contrast = MarketContrastEngine()

    def decide(self, listing: dict):

        deviation = listing.get("market_deviation") or 0.0
        adjusted = listing.get("market_adjusted")
        if adjusted is None:
            adjusted = deviation

        risk = listing.get("risk") or 0.5
        volatility = listing.get("market_volatility") or 0.5
        segment = listing.get("segment") or "unknown"

        # -------------------------
        # BASE PRESSURE
        # -------------------------
        market_pressure = adjusted - risk * 0.25

        # -------------------------
        # CONTRAST
        # -------------------------
        market_pressure = self.contrast.apply(market_pressure, volatility)

        # -------------------------
        # VERDICT
        # -------------------------
        if market_pressure > 0.18:
            verdict = "overpriced"
        elif market_pressure < -0.18:
            verdict = "cheap"
        else:
            verdict = "fair"

        # -------------------------
        # FIXED CONFIDENCE MODEL (IMPORTANT)
        # -------------------------
        # confidence is based on stability, NOT magnitude

        stability = 1.0 - volatility

        signal_strength = max(0.0, 1.0 - abs(market_pressure) / 2.5)

        confidence = stability * signal_strength

        # clamp
        confidence = max(0.05, min(1.0, confidence))

        listing["verdict"] = verdict
        listing["confidence"] = float(confidence)
        listing["market_pressure"] = float(market_pressure)

        return listing
