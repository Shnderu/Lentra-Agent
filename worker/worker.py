import time
import redis

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = "worker-1"

def run():
    print(">>> WORKER LOOP STARTED")

    # 🔥 TEST CONNECTION
    print(">>> REDIS PING:", r.ping())

    while True:
        try:
            print(">>> BEFORE XREADGROUP")

            resp = r.xreadgroup(
                GROUP,
                CONSUMER,
                {STREAM: ">"},
                count=1,
                block=2000
            )

            print(">>> AFTER XREADGROUP")

            if not resp:
                print(">>> NO TASKS")
                continue

            for stream, messages in resp:
                for msg_id, msg in messages:
                    print(f">>> MSG {msg_id}: {msg}")
                    r.xack(STREAM, GROUP, msg_id)

                    r.xadd("stream:rent:results", {
                        "task_id": msg.get("task_id", ""),
                        "status": "done"
                    })

        except Exception as e:
            print(">>> WORKER ERROR:", e)
            time.sleep(2)

if __name__ == "__main__":
    run()
