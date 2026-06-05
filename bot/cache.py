from core.cache_engine import cache


def set_cache(key: str, value, ttl: int = None):
    cache.set(key, value, ttl)


def get_cache(key: str):
    return cache.get(key)


def delete_cache(key: str):
    cache.delete(key)


def clear_cache():
    cache.clear()
