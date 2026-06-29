from lentra.core.market_intelligence.plugins.plugin_contract import MarketPlugin


class ExpatPlugin:

    name = "expat"

    def __init__(self, expat_engine):
        self.engine = expat_engine

    def run(self, obj):

        loc = obj.location

        if isinstance(loc, dict):
            segment = loc.get("segment", "unknown")
        else:
            segment = "unknown"

        obj.signals["expat_score"] = len(segment) * 0.1

        return obj
