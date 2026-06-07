import time
import traceback
from core.engine.postgres_queue import (
    claim_tasks,
    mark_done,
    mark_failed,
    recover_stuck_tasks
)

WORKER_ID = "worker-1"


def process(task):
    print(f"[TASK] {task}")
    time.sleep(1)


def main():
    print("[WORKER] STARTED")

    tick = 0

    while True:
        try:
            # recovery каждые ~30 сек
            if tick % 30 == 0:
                recover_stuck_tasks(300)

            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                print("[WORKER] idle")
                time.sleep(2)
                tick += 1
                continue

            for task in tasks:
                try:
                    process(task)
                    mark_done(task[0])
                except Exception as e:
                    mark_failed(task[0], str(e))
                    print("[TASK ERROR]", traceback.format_exc())

            tick += 1

        except Exception as e:
            print("[WORKER LOOP ERROR]", e)
            time.sleep(3)
            tick += 1


if __name__ == "__main__":
    main()
