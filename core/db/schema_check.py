import os
import psycopg2


REQUIRED_COLUMNS = {
    "tasks": [
        "id",
        "task_type",
        "payload",
        "priority",
        "status",
        "started_at",
        "finished_at",
        "worker_id",
    ]
}


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def validate_schema():
    conn = get_conn()
    cur = conn.cursor()

    for table, columns in REQUIRED_COLUMNS.items():
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table,))

        existing = {r[0] for r in cur.fetchall()}

        missing = [c for c in columns if c not in existing]

        if missing:
            raise RuntimeError(
                f"[SCHEMA ERROR] table={table} missing={missing}"
            )

    conn.close()
