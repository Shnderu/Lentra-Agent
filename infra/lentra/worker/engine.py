import asyncio
import asyncpg
from lentra.db.engine import engine
from lentra.db.queue import PostgresQueue


async def main():
    pool = engine

    queue = PostgresQueue(pool)

    while True:
        try:
            task = await queue.claim_task()

            if not task:
                await asyncio.sleep(1)
                continue

            # ВАЖНО: единый контракт
            task_type = task["task_type"]
            payload = task["payload"]

            print(f"[WORKER] processing {task_type}")

            # TODO: router execution layer
            await queue.mark_done(task["id"])

        except Exception as e:
            print(f"[WORKER LOOP ERROR] {str(e)}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
