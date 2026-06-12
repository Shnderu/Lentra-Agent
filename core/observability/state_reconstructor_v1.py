import redis
import json

"""
Lentra Observable Core v1
State Reconstructor

Главная идея:
→ состояние системы = функция от event log
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"
STREAM_EVENTS = "stream:observability:events"


def reconstruct_state():
    tasks = r.xrange(STREAM_TASKS, "-", "+")
    results = r.xrange(STREAM_RESULTS, "-", "+")
    events = r.xrange(STREAM_EVENTS, "-", "+")

    state = {
        "tasks": len(tasks),
        "results": len(results),
        "events": len(events),
        "lag": len(tasks) - len(results),
    }

    return state


if __name__ == "__main__":
    import json
    print(json.dumps(reconstruct_state(), indent=2))
