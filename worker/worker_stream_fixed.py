import time
import json
import redis
import traceback

STREAM = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = "worker-1"

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def safe_process(msg):
    """
    TODO: plug real business logic here
    """
    return {
        "task_id": msg.get("task_id"),
        "status": "done",
        "result": {"ok": True}
    }


def ensure_group():
    try:
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass


def safe_loop():
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

            for stream, messages in resp:
                for msg_id, msg in messages:

                    print("[MSG]", msg_id, msg)

                    try:
                        result = safe_process(msg)

                        # IMPORTANT: always serialize dict → JSON string
                        r.xadd(
                            "stream:rent:results",
                            {"data": json.dumps(result)}
                        )

                        r.xack(STREAM, GROUP, msg_id)

                        print("[OK]", msg_id)

                    except Exception as e:
                        print("[PROCESS ERROR]", e)
                        print(traceback.format_exc())

                        # retry logic: do NOT ACK
                        time.sleep(1)

        except redis.exceptions.ConnectionError as e:
            print("[REDIS CONNECTION ERROR]", e)
            time.sleep(2)
            reconnect()

        except redis.exceptions.TimeoutError as e:
            print("[REDIS TIMEOUT]", e)
            time.sleep(1)

        except Exception as e:
            print("[FATAL LOOP ERROR]", e)
            print(traceback.format_exc())
            time.sleep(2)


def reconnect():
    global r
    r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)
    ensure_group()


if __name__ == "__main__":
    print("WORKER STARTED (STABLE MODE)")
    safe_loop()
