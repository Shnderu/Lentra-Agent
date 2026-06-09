import psycopg2
import os

DB = {
    "host": "db",
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def conn():
    c = psycopg2.connect(**DB)
    c.autocommit = True
    return c


def get_last_migration():
    cur = conn().cursor()
    cur.execute("""
        SELECT version
        FROM schema_migrations
        ORDER BY applied_at DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    return row[0] if row else None


def rollback_last():
    last = get_last_migration()

    if not last:
        print("[ROLLBACK] nothing to rollback")
        return

    file = f"/app/migrations/{last.replace('.up.sql', '.down.sql')}"

    print("[ROLLBACK]", file)

    cur = conn().cursor()

    with open(file) as f:
        cur.execute(f.read())

    cur.execute("""
        DELETE FROM schema_migrations WHERE version=%s
    """, (last,))


if __name__ == "__main__":
    rollback_last()
