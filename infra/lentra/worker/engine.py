import asyncio
import asyncpg
import os
import traceback

from lentra.db.queue import PostgresQueue


DB_DSN = os.getenv(
    "DATABASE_URL",
    os.getenv("DB_DSN", "postgresql://lentra_user:lentra_password@localhost:5432/lentra")
)


async def main():
    print("[WORKER] STARTED")

    pool = await asyncpg.create_pool(dsn=DB_DSN)
    queue = PostgresQueue(pool)

    while True:
        try:
            task = await queue.claim_task()

            if not task:
                await asyncio.sleep(1)
                continue

            print(f"[WORKER] {task['task_type']}")

            await queue.mark_done(task["id"])

        except Exception as e:
            print(f"[WORKER LOOP ERROR] {e}")
            traceback.print_exc()
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("[WORKER FATAL]", e)
        traceback.print_exc()
    finally:
        print("[WORKER EXIT]")
