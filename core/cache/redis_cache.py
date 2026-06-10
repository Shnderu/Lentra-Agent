import os
import json
import redis.asyncio as redis


class RedisCache:

    def __init__(self):
        self.client = redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0"),
            decode_responses=True
        )

    async def get(self, key: str):
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value, ttl: int = 300):
        await self.client.set(key, json.dumps(value), ex=ttl)
EOFcat << 'EOF' > /opt/flyrum/core/cache/redis_cache.py
import os
import json
import redis.asyncio as redis


class RedisCache:

    def __init__(self):
        self.client = redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0"),
            decode_responses=True
        )

    async def get(self, key: str):
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value, ttl: int = 300):
        await self.client.set(key, json.dumps(value), ex=ttl)
