import psycopg2
import os
import uuid

DB = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def conn():
    c = psycopg2.connect(**DB)
    c.autocommit = True
    return c


def start_workflow(workflow_id, initial_payload):
    c = conn()
    cur = c.cursor()

    trace_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO workflow_runs(workflow_id, status, trace_id)
        VALUES (%s, 'running', %s)
        RETURNING id
    """, (workflow_id, trace_id))

    run_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO workflow_tasks(run_id, node_key, payload)
        VALUES (%s, 'start', %s)
    """, (run_id, initial_payload))

    return run_id, trace_id
