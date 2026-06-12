import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

EVENT_STREAM = "stream:events"


def replay_workflow(wf_id):
    events = r.xrange(EVENT_STREAM, min="-", max="+")

    trace = []

    for _, event in events:
        if event.get("wf_id") == wf_id:
            trace.append(event)

    return trace
