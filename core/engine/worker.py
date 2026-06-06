import time
import traceback
from psycopg2 import OperationalError

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

            print("CLAIMED TASKS:", tasks)

            if not tasks:
                time.sleep(1)
                continue

            for task in tasks:
                try:
                    task_id = task["id"]
                    task_type = task["type"]
                    payload = task["payload"]

                    print("TASK:", task_type, payload)

                    mark_done(task_id)

                except Exception as e:
                    print("TASK ERROR:", repr(e))
                    print(traceback.format_exc())

                    mark_failed(task_id, str(e))

        except OperationalError as db_err:
            print("DB ERROR (retrying):", repr(db_err))
            time.sleep(3)

        except Exception as e:
            print("WORKER LOOP ERROR:", repr(e))
            print(traceback.format_exc())
            time.sleep(2)


if __name__ == "__main__":
    main()
