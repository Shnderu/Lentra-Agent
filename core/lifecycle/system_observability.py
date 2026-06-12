import time
import redis


STREAM_OBS = "stream:observability:system"


class SystemObservability:
    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def emit(self, event_type: str, payload: dict):
        self.r.xadd(
            STREAM_OBS,
            {
                "type": event_type,
                "payload": str(payload),
                "ts": time.time()
            }
        )
