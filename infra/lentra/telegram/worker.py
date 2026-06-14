import time
import psycopg2
import json
import uuid

from lentra.domain.handlers.registry import HANDLERS
from lentra.domain.agent.brain import build_context

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[WORKER RESILIENCE V1.1 - ATOMIC CLAIM] STARTED")

MAX_RETRIES = 3


def claim_tasks():
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'processing',
            started_at = NOW(),
            trace_id = COALESCE(trace_id, gen_random_uuid()::text)
        WHERE id IN (
            SELECT id FROM processing_queue
            WHERE status = 'new'
            ORDER BY id
            FOR UPDATE SKIP LOCKED
            LIMIT 20
        )
        RETURNING id, task_type, payload, retry_count, trace_id;
    """)

    rows = cur.fetchall()
    conn.commit()
    cur.close()
    return rows


def mark_done(task_id, result, trace_id, start_ts):

    latency = int((time.time() - start_ts) * 1000)

    cur = conn.cursor()
    cur.execute("""
        UPDATE processing_queue
        SET status = 'done',
            result = %s::jsonb,
            processed_at = NOW(),
            worker_latency_ms = %s,
            last_error = NULL,
            error_stage = NULL
        WHERE id = %s
    """, (json.dumps(result, ensure_ascii=False), latency, task_id))
    conn.commit()
    cur.close()


def mark_failed(task_id, err, retry_count):

    cur = conn.cursor()

    if retry_count >= MAX_RETRIES:
        cur.execute("""
            UPDATE processing_queue
            SET status = 'dead_letter',
                last_error = %s,
                failed_at = NOW()
            WHERE id = %s
        """, (str(err), task_id))
    else:
        cur.execute("""
            UPDATE processing_queue
            SET status = 'new',
                retry_count = retry_count + 1,
                last_error = %s,
                error_stage = 'worker'
            WHERE id = %s
        """, (str(err), task_id))

    conn.commit()
    cur.close()


def execute(task_type, payload):
    handler = HANDLERS.get(task_type)
    if not handler:
        return {"ux": {"screen": "error"}}

    state = build_context(payload)
    return handler(payload, state)


def main():

    while True:

        tasks = claim_tasks()

        for task_id, task_type, payload, retry_count, trace_id in tasks:

            start_ts = time.time()

            print(f"[EXECUTE] id={task_id} trace={trace_id}")

            try:
                result = execute(task_type, payload)

                if not isinstance(result, dict):
                    raise Exception("invalid_result")

                mark_done(task_id, result, trace_id, start_ts)
                print(f"[DONE] id={task_id}")

            except Exception as e:
                mark_failed(task_id, e, retry_count)
                print(f"[FAILED] id={task_id} err={e}")

        time.sleep(0.2)


if __name__ == "__main__":
    main()
