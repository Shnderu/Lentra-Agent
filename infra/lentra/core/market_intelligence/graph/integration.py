"""
CORE GRAPH INTEGRATION (PURE MODEL)

RULE:
- no runtime imports
- no execution logic
"""

class GraphIntegration:

    def build(self, data: dict):
        return {
            "nodes": data.get("nodes", []),
            "edges": data.get("edges", [])
        }
