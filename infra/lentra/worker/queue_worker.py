import time
import json
import sys

from lentra.core.pipeline.pipeline import LentraPipeline
from lentra.core.queue.task_repository import TaskRepository


def log(*args):
    print(*args, flush=True)


def main():
    log("[QUEUE WORKER] STARTED")

    repo = TaskRepository("postgresql://lentra:lentra@localhost:5432/lentra")
    pipeline = LentraPipeline()

    while True:
        try:
            task = repo.fetch_next()

            if not task:
                time.sleep(2)
                continue

            task_id, payload = task

            log("[TASK]", task_id)

            if isinstance(payload, str):
                payload = json.loads(payload)

            text = payload.get("text", "")

            result = pipeline.run(text)

            repo.mark_done(task_id, result)

            log("[DONE]", task_id)

        except Exception as e:
            log("[ERROR]", task_id if 'task_id' in locals() else None, e)
            try:
                repo.mark_failed(task_id, str(e))
            except:
                pass
            time.sleep(1)


if __name__ == "__main__":
    main()
