import time
import traceback

from lentra.worker.queue import pop_task
from lentra.worker.result_store import save_result
from lentra.core.pipeline.pipeline import LentraPipeline


def log(*args):
    print(*args, flush=True)


def main():
    pipeline = LentraPipeline()

    log("[QUEUE WORKER] STARTED")

    while True:
        task = pop_task()

        if task is None:
            time.sleep(2)
            continue

        task_id = task.get("id")
        query = task.get("query", "")

        try:
            log("[TASK]", task_id)

            # IMPORTANT: pipeline now owns DTO layer
            result = pipeline.run(query)

            save_result(task_id, result)

            log("[DONE]", task_id)

        except Exception:
            log("[ERROR]", task_id)
            traceback.print_exc()

        time.sleep(0.1)


if __name__ == "__main__":
    main()
