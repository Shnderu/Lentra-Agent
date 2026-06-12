import redis
import json
from collections import defaultdict

"""
Lentra Observable Core v2
Causal Graph Builder
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


class CausalGraph:

    def __init__(self):
        self.edges = defaultdict(list)

    def build(self):
        events = r.xrange(STREAM_EVENTS, "-", "+")

        last_event_by_type = {}

        for _, event in events:
            etype = event.get("type")

            # простая причинность:
            # предыдущий event того же типа → текущий
            if etype in last_event_by_type:
                self.edges[last_event_by_type[etype]].append(etype)

            last_event_by_type[etype] = etype

        return self.edges

    def dump(self):
        return json.dumps(self.edges, indent=2)


if __name__ == "__main__":
    g = CausalGraph()
    print(g.dump())
