import redis

def create_redis():
    return redis.Redis(
        host="lentra-redis",
        port=6379,
        decode_responses=True,
        socket_timeout=30,
        socket_connect_timeout=10,
        retry_on_timeout=True,
        health_check_interval=10
    )
