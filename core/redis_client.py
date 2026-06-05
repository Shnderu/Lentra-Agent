import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "flyrum_redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=5,
    retry_on_timeout=True
)
