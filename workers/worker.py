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


def process_task(task: dict):
    """
    Здесь бизнес-логика обработки задачи.
    Пока заглушка (SSA / flight search будет сюда подключаться позже).
    """
    print(f"[TASK] processing id={task['id']} type={task['task_type']}")
    time.sleep(1)


def main():
    print("[WORKER] STARTED")

    # защита от зависших задач при старте
    try:
        recover_stuck_tasks()
    except Exception as e:
        print(f"[RECOVER ERROR] {e}")

    while True:
        try:
            conn = get_conn()

            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                print("[WORKER] idle")
                time.sleep(POLL_INTERVAL)
                continue

            for task in tasks:
                try:
                    process_task(task)
                    mark_done(task["id"])
                except Exception as e:
                    print(f"[TASK ERROR] {e}")
                    mark_failed(task["id"], str(e))

            conn.close()

        except Exception:
            print("[WORKER LOOP ERROR]")
            traceback.print_exc()
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
