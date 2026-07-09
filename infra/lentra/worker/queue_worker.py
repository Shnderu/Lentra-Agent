import time
import traceback
import json

from lentra.worker.queue import pop_task
from lentra.worker.result_store import save_result

from lentra.core.pipeline.worker_search_entrypoint import (
    WorkerSearchEntrypoint
)


def log(*args):
    print(*args, flush=True)


def normalize_payload(payload):

    if isinstance(payload, str):

        try:
            return json.loads(payload)

        except Exception:
            return {
                "query": payload
            }

    if isinstance(payload, dict):
        return payload

    return {
        "query": str(payload)
    }



def main():

    pipeline = WorkerSearchEntrypoint()

    log("[QUEUE WORKER] STARTED")


    while True:

        task = pop_task()


        if task is None:

            time.sleep(2)
            continue


        task_id = task.get(
            "id"
        )

        payload = task.get(
            "payload"
        )


        try:

            log(
                "[TASK]",
                task_id
            )


            payload = normalize_payload(
                payload
            )


            result = pipeline.execute(
                payload
            )


            save_result(
                task_id,
                result
            )


            log(
                "[DONE]",
                task_id
            )


        except Exception:

            log(
                "[ERROR]",
                task_id
            )

            traceback.print_exc()


        time.sleep(0.1)



if __name__ == "__main__":

    main()
