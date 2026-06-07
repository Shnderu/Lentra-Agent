import time
from core.engine.postgres_queue import (
    claim_tasks,
    mark_done,
    mark_failed
)

WORKER_ID = "worker-1"


def main():
    print("POSTGRES WORKER STARTED")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                time.sleep(1)
                continue

            for task in tasks:
                try:
                    print("TASK:", task["type"], task["payload"])

                    # TODO: business logic layer
                    mark_done(task["id"])

                except Exception as e:
                    mark_failed(task["id"], str(e))

        except Exception as e:
            print("WORKER LOOP ERROR:", e)
            time.sleep(2)


if __name__ == "__main__":
    main()
