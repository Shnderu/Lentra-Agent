import time
import traceback
import psycopg2

from lentra.core.pipeline.pipeline import LentraPipeline
from lentra.core.queue.task_repository import TaskRepository

import os


def build_dsn():
    return (
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')} "
        f"host={os.getenv('DB_HOST')} "
        f"port={os.getenv('DB_PORT')}"
    )


def log(*args):
    print(*args, flush=True)


def main():
    dsn = build_dsn()

    repo = TaskRepository(dsn)
    pipeline = LentraPipeline()

    log("[QUEUE WORKER] STARTED")

    while True:
        try:
            task = repo.fetch_next()

            if not task:
                time.sleep(2)
                continue

            task_id, payload = task

            log("[TASK]", task_id)

            try:
                result = pipeline.run(payload)

                repo.mark_done(task_id, result)

                log("[DONE]", task_id)

            except Exception as e:
                repo.mark_failed(task_id, str(e))

                log("[ERROR]", task_id)
                traceback.print_exc()

        except Exception as fatal:
            log("[FATAL WORKER ERROR]")
            traceback.print_exc()
            time.sleep(5)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
