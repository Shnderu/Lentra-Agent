"""
CORE GRAPH PLUGIN = PURE DEFINITION ONLY
NO runtime imports allowed
"""

class GraphPlugin:

    def describe(self):
        return {
            "type": "core_graph_plugin",
            "mode": "static"
        }
