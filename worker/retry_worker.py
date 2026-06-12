import time
import json
import redis

STREAM = "stream:rent:tasks"
GROUP = "workers"


def get_redis():
    return redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def main():
    r = get_redis()

    print("RETRY WORKER V7 STARTED")

    while True:
        pending = r.xpending(STREAM, GROUP)

        # placeholder recovery loop
        print("[DLQ] pending:", pending)

        time.sleep(10)


if __name__ == "__main__":
    main()
