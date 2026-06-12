import time
import redis
import traceback

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM = "stream:rent:tasks"
RESULT = "stream:rent:results"
GROUP = "workers"
CONSUMER = "worker-1"


def emit_error(task_id, stage, e):
    r.xadd("stream:telemetry", {
        "type": "task.error",
        "task_id": task_id,
        "stage": stage,
        "error_type": type(e).__name__,
        "error_msg": str(e),
        "stack": traceback.format_exc()
    })


def emit_success(task_id, stage, latency):
    r.xadd("stream:telemetry", {
        "type": "task.success",
        "task_id": task_id,
        "stage": stage,
        "latency_ms": int(latency * 1000)
    })


def run():
    print(">>> WORKER LOOP STARTED")
    print(">>> REDIS PING:", r.ping())

    while True:
        try:
            resp = r.xreadgroup(
                GROUP,
                CONSUMER,
                {STREAM: ">"},
                count=1,
                block=2000
            )

            if not resp:
                continue

            for _, msgs in resp:
                for msg_id, msg in msgs:

                    start = time.time()
                    task_id = msg.get("task_id")

                    try:
                        # simulate processing
                        result = {
                            "task_id": task_id,
                            "status": "done"
                        }

                        r.xadd(RESULT, result)
                        r.xack(STREAM, GROUP, msg_id)

                        emit_success(task_id, "worker", time.time() - start)

                    except Exception as e:
                        emit_error(task_id, "worker", e)

        except Exception as e:
            print("[FATAL]", e)
            time.sleep(2)


if __name__ == "__main__":
    run()

# OBSERVABILITY HOOK (v1)
from core.observability.event_bus_v1 import bus

def emit_task_event(msg):
    bus.emit("task.processed", msg)
