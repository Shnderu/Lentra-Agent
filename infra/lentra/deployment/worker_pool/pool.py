# ============================================================
# WORKER POOL V17.2
# ============================================================

import asyncio


class WorkerPool:
    def __init__(self, workers=3):
        self.workers = workers
        self.queue = asyncio.Queue()

    async def add_task(self, task):
        await self.queue.put(task)

    async def worker(self, handler):
        while True:
            task = await self.queue.get()

            try:
                await handler(task)
            except Exception as e:
                print(f"[WORKER ERROR] {e}")

            self.queue.task_done()

    async def start(self, handler):
        tasks = [
            asyncio.create_task(self.worker(handler))
            for _ in range(self.workers)
        ]

        await asyncio.gather(*tasks)
