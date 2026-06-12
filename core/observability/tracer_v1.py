import time
import uuid
import redis

"""
Lentra Observable Core v1
Distributed Trace Layer
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TRACES = "stream:observability:traces"


class Trace:

    def __init__(self, name):
        self.trace_id = str(uuid.uuid4())
        self.name = name
        self.start = time.time()

    def span(self, span_name, meta=None):
        r.xadd(STREAM_TRACES, {
            "trace_id": self.trace_id,
            "span": span_name,
            "ts": time.time(),
            "meta": meta or {}
        })

    def finish(self):
        r.xadd(STREAM_TRACES, {
            "trace_id": self.trace_id,
            "span": "FINISH",
            "duration": time.time() - self.start
        })


def start_trace(name):
    return Trace(name)


if __name__ == "__main__":
    t = start_trace("demo")
    t.span("step1")
    t.span("step2")
    t.finish()
