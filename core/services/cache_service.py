import redis
import json
import hashlib


class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )

        self.ttl = 300  # 5 минут кеш

    def _key(self, text: str) -> str:
        return "cache:" + hashlib.md5(text.encode()).hexdigest()

    def get(self, text: str):
        key = self._key(text)
        data = self.client.get(key)

        if data:
            return json.loads(data)

        return None

    def set(self, text: str, value: dict):
        key = self._key(text)
        self.client.setex(key, self.ttl, json.dumps(value))


cache_service = CacheService()
