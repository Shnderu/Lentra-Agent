import redis
from bot.core.config import settings

client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def get_cache(key: str):
    return client.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    client.set(key, value, ex=ttl)
