import redis
import time
import json
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)


OBS_STREAM = "stream:system:observe"
MUTATION_STREAM = "stream:system:mutations"


def observe():
    events = r.xrevrange(OBS_STREAM, count=50)
    return events


def analyze(events):
    failures = 0
    load = 0

    for _, e in events:
        if "error" in str(e):
            failures += 1
        if e.get("metric") == "load":
            load += float(e.get("value", 0))

    return {"failures": failures, "load": load}


def decide(state):
    if state["failures"] > 5:
        return "mutate_fallback_strategy"

    if state["load"] > 80:
        return "scale_architecture"

    return "optimize"


def mutate(action):
    r.xadd(MUTATION_STREAM, {
        "action": action,
        "ts": time.time()
    })


def loop():
    print("LEVEL 19 OS KERNEL ACTIVE")

    while True:
        events = observe()
        state = analyze(events)
        action = decide(state)

        mutate(action)

        time.sleep(5)


if __name__ == "__main__":
    loop()
