

class PriceForecastEngine:

    def forecast(self, market_price: float, area_score: dict, risk: float):

        base = market_price

        # 1. area pressure (demand proxy)
        demand = area_score.get("expat_density", 5) / 10

        # 2. infrastructure quality boosts price
        infra = area_score.get("internet", 5) / 10

        # 3. risk suppresses demand
        risk_factor = 1 - risk

        # trend model (simple but stable)
        trend = (demand * 0.6 + infra * 0.4) * risk_factor

        # projected growth rate
        growth_rate = (trend - 0.5) * 0.2  # bounded sensitivity

        price_30d = base * (1 + growth_rate)
        price_90d = base * (1 + growth_rate * 2.5)

        return {
            "trend_score": round(trend, 3),
            "growth_rate": round(growth_rate, 4),

            "forecast_30d": round(price_30d, 2),
            "forecast_90d": round(price_90d, 2),

            "interpretation": self._interpret(trend)
        }


    def _interpret(self, trend):

        if trend > 0.7:
            return "hot_market"
        elif trend > 0.5:
            return "stable_market"
        else:
            return "declining_market"
