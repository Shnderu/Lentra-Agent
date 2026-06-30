import asyncio
import socket

from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.intelligence_gateway import interpret

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

            # --------------------------------------------
            # 1. NORMAL EXECUTION (FLOW GLUE)
            # --------------------------------------------
            raw_result = flow_glue.run(flow)

            # --------------------------------------------
            # 2. INTELLIGENCE POST-PROCESSING LAYER
            # --------------------------------------------
            enriched = interpret({
                "task": flow.get("type", "unknown"),
                "input": flow,
                "output": raw_result,
                "worker_id": WORKER_ID
            })

            # --------------------------------------------
            # 3. FINALIZE TASK
            # --------------------------------------------
            repo.mark_done(task_id, result=enriched)

        except Exception as e:
            print("[WORKER ERROR]", e)
            repo.mark_failed(task_id)


async def main():
    await run_worker()


if __name__ == "__main__":
    asyncio.run(main())
