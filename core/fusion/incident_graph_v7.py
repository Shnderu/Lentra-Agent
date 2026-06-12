import redis
from collections import defaultdict

"""
Lentra Fusion Core v7
Unified Incident Graph
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"
STREAM_ERRORS = "stream:diagnostics:errors"
STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


class IncidentGraph:

    def build(self):
        events = r.xrange(STREAM_EVENTS, "-", "+")
        errors = r.xrange(STREAM_ERRORS, "-", "+")
        tasks = r.xrange(STREAM_TASKS, "-", "+")
        results = r.xrange(STREAM_RESULTS, "-", "+")

        graph = {
            "nodes": [],
            "edges": []
        }

        node_index = 0

        for _, e in events:
            graph["nodes"].append({"id": f"e{node_index}", "type": "event", "data": e})
            node_index += 1

        for _, e in errors:
            graph["nodes"].append({"id": f"x{node_index}", "type": "error", "data": e})
            node_index += 1

        for _, t in tasks:
            graph["nodes"].append({"id": f"t{node_index}", "type": "task", "data": t})
            node_index += 1

        for _, r_ in results:
            graph["nodes"].append({"id": f"r{node_index}", "type": "result", "data": r_})
            node_index += 1

        for i in range(len(graph["nodes"]) - 1):
            graph["edges"].append({
                "from": graph["nodes"][i]["id"],
                "to": graph["nodes"][i + 1]["id"]
            })

        return graph


if __name__ == "__main__":
    import json
    print(json.dumps(IncidentGraph().build(), indent=2))
