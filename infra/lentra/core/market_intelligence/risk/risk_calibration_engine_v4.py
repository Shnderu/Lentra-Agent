class RiskCalibrationEngineV4:

    """
    Smooth probabilistic risk calibration
    """

    def calibrate(self, listing: dict) -> dict:

        base_risk = listing.get("risk", 0.5)

        price = listing.get("price", 0)
        market = listing.get("market_price", price)

        deviation = abs(price - market) / (market + 1)

        calibrated = base_risk + (deviation * 0.3)

        listing["risk_calibrated"] = min(max(calibrated, 0), 1)

        return listing
