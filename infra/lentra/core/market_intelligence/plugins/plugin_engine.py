from lentra.core.market_intelligence.plugins.plugin_registry import PluginRegistry
from lentra.core.market_intelligence.contracts.object_builder import MarketObjectBuilder


class PluginEngine:

    def __init__(self):
        self.builder = MarketObjectBuilder()
        self.registry = PluginRegistry()

    def register_plugin(self, plugin):
        self.registry.register(plugin)

    def analyze(self, listings):

        results = []

        for item in listings:

            obj = self.builder.build(item)

            # =========================
            # STEP H: GRAPH EXECUTION
            # =========================
            obj = self.registry.execute(obj)

            results.append(obj.__dict__)

        return results
