import os
import redis
from core.reliability.idempotency import IdempotencyStore

REDIS_HOST = os.getenv("REDIS_HOST", "lentra-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

idem = IdempotencyStore(r)

def main():
    print("LENTRA WORKER STARTED (V6.6 PRODUCTION MODE)")

    while True:
        # placeholder loop (stream consumer in next versions)
        pass


if __name__ == "__main__":
    main()
