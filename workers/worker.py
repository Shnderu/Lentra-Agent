import time

from core.engine.postgres_queue import (
    get_conn,
    claim_tasks,
    mark_done,
    mark_failed,
)

from core.router import route_task


WORKER_ID = "worker-1"


def main():
    print("[WORKER] STARTED")

    conn = get_conn()

    while True:
        try:
            tasks = claim_tasks(conn, WORKER_ID, limit=5)

            if not tasks:
                print("[WORKER] idle")
                time.sleep(1)
                continue

            for task in tasks:
                print(f"[TASK] executing id={task['id']} type={task['task_type']}")

                result = route_task(task, conn)

                mark_done(conn, task["id"])

                print(f"[TASK] done id={task['id']}")

        except Exception as e:
            print(f"[WORKER LOOP ERROR] {e}")
            mark_failed(conn, task["id"] if 'task' in locals() else 0)
            time.sleep(2)


if __name__ == "__main__":
    main()
