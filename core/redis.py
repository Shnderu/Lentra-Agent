import os
import redis

# ВАЖНО: имя должно совпадать с docker-compose service name
REDIS_URL = os.getenv("REDIS_URL", "redis://flyrum_redis:6379")

r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    health_check_interval=30,
    socket_connect_timeout=5,
    retry_on_timeout=True
)
