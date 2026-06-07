import time
import traceback

from core.engine.postgres_queue import (
    get_conn,
    claim_tasks,
    mark_done,
    mark_failed,
    recover_stuck_tasks,
)

WORKER_ID = "worker-1"
POLL_INTERVAL = 2


# ----------------------------
# RUNTIME METRICS (in-memory v1)
# ----------------------------
processed_count = 0
failed_count = 0


def process_task(task: dict):
    """
    Бизнес-логика обработки задачи.
    Пока заглушка.
    """
    print(f"[TASK] processing id={task['id']} type={task['task_type']}")
    time.sleep(1)


def main():
    global processed_count, failed_count

    print("[WORKER] STARTED")

    try:
        recover_stuck_tasks()
    except Exception as e:
        print(f"[RECOVER ERROR] {e}")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                print("[WORKER] idle")
                time.sleep(POLL_INTERVAL)
                continue

            for task in tasks:
                try:
                    process_task(task)
                    mark_done(task["id"])

                    processed_count += 1

                except Exception as e:
                    print(f"[TASK ERROR] {e}")
                    mark_failed(task["id"])

                    failed_count += 1

            print(f"[WORKER METRICS] processed={processed_count} failed={failed_count}")

        except Exception:
            print("[WORKER LOOP ERROR]")
            traceback.print_exc()
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
