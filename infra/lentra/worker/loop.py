import asyncio
import socket
from lentra.core.di.container import build_container

WORKER_ID = socket.gethostname()

async def run_worker():
    container = build_container()

    repo = container["tasks_repository"]
    flow_glue = container["flow_glue"]

    print("[WORKER] STARTED:", WORKER_ID)

    while True:
        task = repo.fetch_next()

        if not task:
            await asyncio.sleep(1)
            continue

        task_id = task["id"]

        try:
            repo.mark_processing(task_id, WORKER_ID)

            flow = task["flow"]
            flow_glue.run(flow)

            repo.mark_done(task_id)

        except Exception as e:
            print("[ERROR]", e)
            repo.mark_failed(task_id)

async def main():
    await run_worker()

if __name__ == "__main__":
    asyncio.run(main())
