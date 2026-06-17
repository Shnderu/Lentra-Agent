# ============================================================
# LENTRA WORKER ENGINE V15.7 (POOL FIX)
# ============================================================

import asyncio
import logging
from typing import Dict, Any

import asyncpg

from lentra.rent.domain_v1 import create_rent_router
from lentra.db.queue import PostgresQueue

logger = logging.getLogger("lentra.worker")

router = create_rent_router()


class WorkerEngine:
    def __init__(self, queue: PostgresQueue):
        self.queue = queue
        self.running = True

    async def process(self, task: Dict[str, Any]):
        result = await router.route(task)
        await self.queue.mark_done(task["id"])
        return result

    async def run(self):
        logger.info("[WORKER] started")

        while self.running:
            try:
                task = await self.queue.claim_task()

                if not task:
                    await asyncio.sleep(1)
                    continue

                try:
                    await self.process(task)

                except Exception as e:
                    await self.queue.mark_failed(
                        task["id"],
                        str(e),
                        task.get("attempts", 0),
                    )

            except Exception as loop_error:
                logger.error(f"[WORKER LOOP ERROR] {loop_error}")
                await asyncio.sleep(2)


def create_worker(queue: PostgresQueue) -> WorkerEngine:
    return WorkerEngine(queue)


# ============================================================
# ENTRYPOINT FIXED (POOL INITIALIZATION)
# ============================================================

async def main():
    pool = await asyncpg.create_pool(
        user="postgres",
        password="postgres",
        database="lentra",
        host="localhost",
        port=5432,
        min_size=1,
        max_size=5,
    )

    queue = PostgresQueue(pool)

    worker = WorkerEngine(queue)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
