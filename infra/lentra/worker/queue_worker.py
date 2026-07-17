import time
import traceback
import json

import psycopg2

from lentra.core.data.fetcher import TaskFetcher

from lentra.core.pipeline.worker_search_entrypoint import (
    WorkerSearchEntrypoint
)


DSN = "postgresql://lentra:lentra@localhost:5432/lentra"


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

        if "query" not in payload:

            if "text" in payload:
                payload["query"] = payload["text"]

        return payload


    return {
        "query": str(payload)
    }



def save_result(task_id, result):

    conn = psycopg2.connect(DSN)

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET payload = payload || %s::jsonb,
            status = 'done'
        WHERE id = %s
        """,
        (
            json.dumps(
                {
                    "pipeline_result": result
                },
                default=str
            ),
            task_id,
        )
    )

    conn.commit()

    cur.close()
    conn.close()



def mark_failed(task_id, error):

    conn = psycopg2.connect(DSN)

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status='dead',
            payload = payload || %s::jsonb
        WHERE id=%s
        """,
        (
            json.dumps(
                {
                    "worker_error": error
                }
            ),
            task_id,
        )
    )

    conn.commit()

    cur.close()
    conn.close()



def main():

    fetcher = TaskFetcher(DSN)

    pipeline = WorkerSearchEntrypoint()

    log("[QUEUE WORKER] STARTED")


    while True:

        task = fetcher.fetch_and_lock()


        if task is None:

            time.sleep(2)
            continue


        task_id = task["id"]
        payload = task["payload"]
        attempts = task.get("retry_count", 0)


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


            mark_failed(
                task_id,
                "worker_error"
            )


        time.sleep(0.1)



if __name__ == "__main__":

    main()
