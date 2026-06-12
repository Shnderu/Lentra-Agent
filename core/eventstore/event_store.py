import redis
import json
import time

class EventStore:
    """
    Append-only event log.
    Source of truth for full system reconstruction.
    """

    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.key = "event:log"

    # -----------------------------
    # APPEND EVENT
    # -----------------------------
    def append(self, event_type, task_id, payload=None):
        event = {
            "type": event_type,
            "task_id": task_id,
            "payload": payload or {},
            "ts": time.time()
        }

        self.r.xadd(self.key, event)
        return event

    # -----------------------------
    # READ EVENTS
    # -----------------------------
    def tail(self, count=100):
        return self.r.xrevrange(self.key, count=count)

    # -----------------------------
    # REBUILD STATE (future use)
    # -----------------------------
    def replay(self):
        events = self.r.xrange(self.key)
        state = {}

        for _, e in events:
            tid = e["task_id"]
            state.setdefault(tid, []).append(e)

        return state
