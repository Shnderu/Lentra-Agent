# ============================================================
# WORKER ENTRYPOINT V17.2
# ============================================================

import asyncio
from lentra.deployment.worker_pool.pool import WorkerPool


async def process(task):
    print(f"[WORKER] processing {task}")


async def main():
    pool = WorkerPool(workers=5)
    await pool.start(process)


if __name__ == "__main__":
    asyncio.run(main())
