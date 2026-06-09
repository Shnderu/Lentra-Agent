import os
import psycopg2

MIGRATIONS = [
    "001_init.sql",
]


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def ensure_lock_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT NOW()
        );
    """)


def is_applied(cur, version):
    cur.execute(
        "SELECT 1 FROM schema_migrations WHERE version = %s",
        (version,)
    )
    return cur.fetchone() is not None


def mark_applied(cur, version):
    cur.execute(
        "INSERT INTO schema_migrations(version) VALUES (%s)",
        (version,)
    )


def apply_migration(cur, path):
    with open(path, "r") as f:
        sql = f.read()
    cur.execute(sql)


def run_migrations():
    conn = get_conn()
    conn.autocommit = True
    cur = conn.cursor()

    ensure_lock_table(cur)

    for migration in MIGRATIONS:
        if is_applied(cur, migration):
            continue

        path = f"/app/migrations/{migration}"

        print(f"[MIGRATION] applying {migration}")

        apply_migration(cur, path)
        mark_applied(cur, migration)

        print(f"[MIGRATION] done {migration}")

    conn.close()
