from collections import defaultdict

"""
Lentra Fusion Core v7
Incident Correlation Engine
"""


class IncidentCorrelation:

    def correlate(self, graph):
        correlations = defaultdict(list)

        nodes = graph["nodes"]

        for i in range(len(nodes) - 1):
            a = nodes[i]
            b = nodes[i + 1]

            key = (a["type"], b["type"])
            correlations[key].append((a["id"], b["id"]))

        return {
            "correlations": dict(correlations)
        }


if __name__ == "__main__":
    print("Correlation engine ready")
