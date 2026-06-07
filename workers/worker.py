import time
import traceback
from core.engine.postgres_queue import claim_tasks, mark_done, mark_failed

WORKER_ID = "worker-1"


def process(task):
    """
    TODO: сюда позже подключим flight_engine
    """
    print(f"[TASK] {task}")
    time.sleep(1)


def main():
    print("[WORKER] STARTED")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                time.sleep(2)
                continue

            for task in tasks:
                try:
                    process(task)
                    mark_done(task["id"])
                except Exception as e:
                    mark_failed(task["id"], str(e))
                    print("[TASK ERROR]", traceback.format_exc())

        except Exception as e:
            print("[WORKER LOOP ERROR]", e)
            time.sleep(3)


if __name__ == "__main__":
    main()
