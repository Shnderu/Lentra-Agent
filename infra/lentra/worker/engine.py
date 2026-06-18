import asyncio
import asyncpg
import os
import traceback

from lentra.db.queue import PostgresQueue

DB_DSN = os.getenv("DB_DSN")


async def restore_stuck_tasks(pool):
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            UPDATE processing_queue
            SET
                status = 'pending',
                updated_at = NOW()
            WHERE
                status = 'processing'
                AND updated_at < NOW() - INTERVAL '10 minutes'
            """
        )

    restored = int(result.split()[-1])

    if restored > 0:
        print(f"[WORKER] Restored {restored} stuck tasks")
    else:
        print("[WORKER] No stuck tasks found")


async def process_task(task):
    task_type = task["task_type"]

    print(f"[WORKER] {task_type}")

    # simulate work
    await asyncio.sleep(0.1)


async def worker_loop():
    pool = await asyncpg.create_pool(
        dsn=DB_DSN,
        min_size=1,
        max_size=10,
    )

    await restore_stuck_tasks(pool)

    queue = PostgresQueue(pool)

    print("[WORKER] STARTED")

    while True:
        try:
            task = await queue.claim_task()

            if not task:
                await asyncio.sleep(1)
                continue

            try:
                await process_task(task)

                await queue.mark_done(task["id"])

            except Exception as e:
                print("[WORKER TASK ERROR]", str(e))
                traceback.print_exc()

                await queue.mark_failed(
                    task["id"],
                    str(e),
                )

        except Exception as e:
            print("[WORKER LOOP ERROR]", str(e))
            traceback.print_exc()

            await asyncio.sleep(2)


async def main():
    while True:
        try:
            await worker_loop()

        except Exception as e:
            print("[WORKER FATAL RESTART]", str(e))
            traceback.print_exc()

            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
