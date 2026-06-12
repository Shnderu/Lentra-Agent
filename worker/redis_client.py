import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "lentra-redis")

def get_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True,
        socket_timeout=10,
        socket_connect_timeout=10,
        health_check_interval=30,
        retry=redis.Retry(redis.ExponentialBackoff(), 3)
    )
