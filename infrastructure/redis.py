import os
import redis

_redis = None

def get_redis():
    global _redis

    if _redis is None:
        _redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "lentra-redis"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            decode_responses=True
        )

    return _redis
