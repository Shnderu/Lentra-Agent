import redis

"""
Lentra Observable Core v2
Failure Timeline Builder
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


def timeline():
    events = r.xrange(STREAM_EVENTS, "-", "+")

    timeline = []

    for ts, e in events:
        timeline.append({
            "type": e.get("type"),
            "ts": e.get("ts"),
            "event_id": ts
        })

    return timeline


if __name__ == "__main__":
    import json
    print(json.dumps(timeline(), indent=2))
