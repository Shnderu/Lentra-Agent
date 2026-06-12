import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

AGENTS = "stream:agents:events"


def evaluate_population():
    events = r.xrevrange(AGENTS, count=200)

    stats = {}

    for _, e in events:
        aid = e.get("agent_id")
        if aid not in stats:
            stats[aid] = {"success": 0, "fail": 0}

        if e.get("result") == "success":
            stats[aid]["success"] += 1
        else:
            stats[aid]["fail"] += 1

    return stats


def evolve():
    stats = evaluate_population()

    for agent, s in stats.items():
        if s["fail"] > s["success"] * 2:
            r.xadd("stream:agents:kill", {"agent_id": agent})
        elif s["success"] > s["fail"] * 2:
            r.xadd("stream:agents:clone", {"agent_id": agent})
