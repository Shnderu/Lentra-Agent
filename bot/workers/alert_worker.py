import time
import os
from core.engine.repository import fetch_tasks, mark_done, mark_failed


WORKER_ID = os.getenv("HOSTNAME", "worker-unknown")


def process_task(task):
    try:
        print(f"[WORKER {WORKER_ID}] task: {task['id']}")

        payload = task.get("payload", {})
        print("[PAYLOAD]", payload)

        mark_done(task["id"])

    except Exception as e:
        print("[WORKER ERROR]", e)
        mark_failed(task["id"])


def run_worker():
    print(">>> WORKER STARTED")

    while True:
        try:
            # 🔴 FIX: теперь передаём worker_id
            tasks = fetch_tasks(worker_id=WORKER_ID)

            if not tasks:
                time.sleep(2)
                continue

            for task in tasks:
                process_task(task)

        except Exception as e:
            print("[WORKER LOOP ERROR]", e)
            time.sleep(3)


if __name__ == "__main__":
    run_worker()
