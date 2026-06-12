import redis
from collections import defaultdict

"""
Lentra Observable Core v4
Self-Explaining Engine

Преобразует event graph → human-readable incident story
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


class Explainer:

    def load_events(self):
        return r.xrange(STREAM_EVENTS, "-", "+")

    def build_chain(self):
        events = self.load_events()

        chain = []
        last = None

        for _, e in events:
            etype = e.get("type")
            ts = e.get("ts")

            node = {
                "event": etype,
                "ts": ts,
                "cause": last
            }

            chain.append(node)
            last = etype

        return chain

    def explain(self):
        chain = self.build_chain()

        if not chain:
            return {"summary": "No events recorded"}

        summary = []
        summary.append("SYSTEM INCIDENT REPORT")
        summary.append("--------------------------------")

        for i, node in enumerate(chain):
            line = f"{i+1}. Event: {node['event']}"

            if node["cause"]:
                line += f" → triggered after {node['cause']}"

            summary.append(line)

        return {
            "summary": "\n".join(summary),
            "chain_length": len(chain)
        }


if __name__ == "__main__":
    import json
    print(json.dumps(Explainer().explain(), indent=2))
