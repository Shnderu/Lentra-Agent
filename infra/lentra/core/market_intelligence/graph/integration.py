"""
CORE GRAPH INTEGRATION

ROLE:
- pure graph representation
- enrichment only

NO:
- execution
- orchestration
- engine calls
"""


class GraphIntegration:

    def build(self, data: dict):

        return {
            "nodes": data.get("nodes", []),
            "edges": data.get("edges", []),
            "status": "graph_enrichment_only",
        }


def try_graph_execute(engines, payload):

    return {
        "graph": {
            "status": "skipped",
            "reason": "graph_is_enrichment_only",
        }
    }
