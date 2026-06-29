from typing import List
from lentra.core.market_intelligence.plugins.plugin_contract import MarketPlugin


class PluginRegistry:

    def __init__(self):
        self.plugins: List[MarketPlugin] = []

    def register(self, plugin: MarketPlugin):
        self.plugins.append(plugin)

    def execute(self, obj):

        for plugin in self.plugins:
            obj = plugin.run(obj)

        return obj
