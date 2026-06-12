import time
import json
import traceback
from redis.exceptions import TimeoutError, ConnectionError
from redis_client import create_redis

STREAM = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = "worker-1"

r = create_redis()


def ensure_group():
    try:
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass


def process(msg):
    return {
        "task_id": msg.get("task_id"),
        "status": "done"
    }


def loop():
    ensure_group()

    while True:
        try:
            resp = r.xreadgroup(
                GROUP,
                CONSUMER,
                {STREAM: ">"},
                count=1,
                block=5000
            )

            if not resp:
                continue

            for _, messages in resp:
                for msg_id, msg in messages:
                    try:
                        result = process(msg)

                        r.xadd(
                            "stream:rent:results",
                            {"data": json.dumps(result)}
                        )

                        r.xack(STREAM, GROUP, msg_id)

                    except Exception:
                        print("[PROCESS ERROR]", traceback.format_exc())
                        time.sleep(1)

        except TimeoutError:
            print("[REDIS TIMEOUT SAFE IGNORE]")
            time.sleep(1)
            continue

        except ConnectionError:
            print("[REDIS RECONNECT]")
            global r
            r = create_redis()
            ensure_group()
            time.sleep(2)

        except Exception:
            print("[FATAL]", traceback.format_exc())
            time.sleep(2)


if __name__ == "__main__":
    print("WORKER STARTED (HARDENED MODE)")
    loop()
