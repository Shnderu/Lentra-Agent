from lentra.core.market_intelligence.plugins.plugin_contract import MarketPlugin


class ComparisonPlugin:

    name = "comparison"

    def run(self, obj):

        price = obj.price
        market_price = obj.market_price or price

        obj.deviation = ((price - market_price) / max(market_price, 1)) * 100

        obj.signals["comparison_score"] = 1.0 - abs(obj.deviation) / 100

        return obj
