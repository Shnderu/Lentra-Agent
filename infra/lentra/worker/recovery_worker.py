import time
import json
import traceback
from lentra.storage.db import get_conn
from lentra.core.pipeline.pipeline import LentraPipeline
from lentra.core.contracts.v1.task_state import TaskState
from lentra.core.contracts.v1.task_state_service import TaskStateService
from lentra.core.contracts.v1.retry_policy import should_retry


state = TaskStateService()


def log(*args):
    print("[RECOVERY]", *args, flush=True)


def fetch_failed_batch(limit=20):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload, retry_count
        FROM tasks
        WHERE status = 'failed'
        ORDER BY created_at ASC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def normalize(payload):
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            return {"text": payload}
    return payload


def increment_retry(task_id, retry_count, error):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET retry_count = %s,
            payload = payload || %s
        WHERE id = %s
    """, (retry_count, json.dumps({"last_error": error}), task_id))

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("[RECOVERY WORKER ENTRYPOINT HIT]")
    pipeline = LentraPipeline()

    log("STARTED")

    while True:
        try:
            batch = fetch_failed_batch(10)

            if not batch:
                time.sleep(10)
                continue

            for task_id, payload, retry_count in batch:

                try:
                    log("RECOVER", task_id)

                    if not should_retry(retry_count):
                        state.set_status(
                            task_id,
                            TaskState.DEAD,
                            {"reason": "retry_limit_exceeded"}
                        )
                        log("DEAD (retry limit)", task_id)
                        continue

                    state.set_status(
                        task_id,
                        TaskState.RECOVERING,
                        {"retry": retry_count}
                    )

                    clean = normalize(payload)

                    result = pipeline.run(clean)

                    state.set_status(
                        task_id,
                        TaskState.DONE,
                        {"recovered": True}
                    )

                    log("RECOVERED", task_id)

                except Exception as e:
                    traceback.print_exc()

                    new_retry = retry_count + 1

                    increment_retry(task_id, new_retry, str(e))

                    state.set_status(
                        task_id,
                        TaskState.FAILED,
                        {
                            "error": str(e),
                            "retry": new_retry
                        }
                    )

                    log("FAILED AGAIN", task_id)

            time.sleep(2)

        except Exception:
            traceback.print_exc()
            time.sleep(5)


if __name__ == "__main__":
    main()
