import redis
from collections import Counter, defaultdict

"""
Lentra Observable Core v2
Root Cause Analysis Engine (non-AI deterministic)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


class RCAEngine:

    def analyze(self):
        events = r.xrange(STREAM_EVENTS, "-", "+")

        failures = []
        causes = defaultdict(list)

        for _, e in events:
            etype = e.get("type")

            if "error" in etype or "fail" in etype:
                failures.append(e)

                context = e.get("payload", {})
                cause_hint = context.get("cause", "unknown")

                causes[cause_hint].append(etype)

        return {
            "total_failures": len(failures),
            "cause_clusters": dict(causes),
            "top_cause": Counter(c for c in causes).most_common(1)
        }


if __name__ == "__main__":
    import json
    print(json.dumps(RCAEngine().analyze(), indent=2))
