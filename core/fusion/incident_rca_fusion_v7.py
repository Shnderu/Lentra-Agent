import json
from core.fusion.incident_graph_v7 import IncidentGraph
from core.fusion.incident_correlation_v7 import IncidentCorrelation

"""
Lentra Fusion Core v7
RCA + Diagnostics Fusion Layer
"""


class IncidentRCAFusion:

    def run(self):
        graph = IncidentGraph().build()

        corr = IncidentCorrelation().correlate(graph)

        severity = self._compute_severity(graph)

        return {
            "severity": severity,
            "graph_size": len(graph["nodes"]),
            "edges": len(graph["edges"]),
            "correlations": corr
        }

    def _compute_severity(self, graph):
        error_nodes = [n for n in graph["nodes"] if n["type"] == "error"]

        if len(error_nodes) == 0:
            return "NONE"
        elif len(error_nodes) < 3:
            return "LOW"
        elif len(error_nodes) < 10:
            return "MEDIUM"
        else:
            return "HIGH"


if __name__ == "__main__":
    fusion = IncidentRCAFusion()
    print(json.dumps(fusion.run(), indent=2))
