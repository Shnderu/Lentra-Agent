from collections import defaultdict

class IncidentCorrelation:

    def correlate(self, graph):
        correlations = defaultdict(list)

        nodes = graph["nodes"]

        for i in range(len(nodes) - 1):
            a = nodes[i]
            b = nodes[i + 1]

            key = f"{a['type']}->{b['type']}"   # FIX: STRING KEY
            correlations[key].append({
                "from": a["id"],
                "to": b["id"]
            })

        return {"correlations": dict(correlations)}
