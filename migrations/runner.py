import psycopg2
import os
import glob
from migrations.lock import acquire_lock, release_lock

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


def init():
    cur = conn().cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS system_versions (
            version TEXT PRIMARY KEY,
            deployed_at TIMESTAMP DEFAULT NOW()
        );
    """)


def applied():
    cur = conn().cursor()
    cur.execute("SELECT version FROM schema_migrations")
    return set(r[0] for r in cur.fetchall())


def apply(sql_file):
    cur = conn().cursor()
    with open(sql_file) as f:
        cur.execute(f.read())


def mark(version):
    cur = conn().cursor()
    cur.execute("""
        INSERT INTO schema_migrations(version)
        VALUES (%s)
        ON CONFLICT DO NOTHING;
    """, (version,))


def register(version):
    cur = conn().cursor()
    cur.execute("""
        INSERT INTO system_versions(version)
        VALUES (%s)
        ON CONFLICT DO NOTHING;
    """, (version,))


def run():
    print("[V11 MIGRATIONS START]")

    init()

    print("[LOCK] acquiring redis lock")
    acquire_lock()

    try:
        done = applied()

        files = sorted(glob.glob("/app/migrations/*.up.sql"))

        for f in files:
            v = f.split("/")[-1]

            if v in done:
                continue

            print("[APPLY]", v)

            apply(f)
            mark(v)
            register(v)

        print("[V11 MIGRATIONS DONE]")

    finally:
        print("[LOCK] release")
        release_lock()


if __name__ == "__main__":
    run()
