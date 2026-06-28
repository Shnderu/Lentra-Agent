
from lentra.core.market_intelligence.forecast.price_forecast_engine import PriceForecastEngine


class ForecastModule:

    def __init__(self):
        self.engine = PriceForecastEngine()

    def run(self, ctx):

        ctx.forecast = self.engine.forecast(
            market_price=600,
            area_score={"expat_density": 5, "internet": 5},
            risk=0.5
        )

        return ctx
