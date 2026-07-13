class RankingEngineV3:

    def score(self, listing):

        ranking = {}

        price = listing.get("price", 0)
        market_price = listing.get("market_price", 1)

        prediction = listing.get("prediction", {})
        predicted_price = prediction.get("predicted_price", market_price)

        # price factor
        price_factor = max(0.1, 1 - abs(price - market_price) / max(market_price, 1))

        # prediction delta impact (NEW STEP 6)
        pred_delta = 1 - abs(price - predicted_price) / max(predicted_price, 1)
        pred_delta = max(0.1, pred_delta)

        # risk
        risk = listing.get("risk_calibrated", 0.5)

        risk_weight = 1 - risk

        # final attractiveness (STEP 6 ENHANCED)
        attractiveness = (
            price_factor * 0.4 +
            pred_delta * 0.4 +
            risk_weight * 0.2
        )

        ranking["attractiveness"] = attractiveness
        ranking["price_factor"] = price_factor
        ranking["prediction_factor"] = pred_delta
        ranking["risk_weight"] = risk_weight

        return ranking
