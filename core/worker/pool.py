import asyncio
import os

from core.queue.queue import claim, ack, fail


WORKER_ID = os.getenv("WORKER_ID", "pool-manager")


# -----------------------------
# TASK ROUTER (POOL LEVEL)
# -----------------------------
async def process_task(task):

    ttype = task["type"]

    # ROUTE SEARCH
    if ttype == "route_search":
        return await route_worker(task)

    # DEALS
    if ttype == "deal_search":
        return await deal_worker(task)

    # AI PLANNER
    if ttype == "ai_planner":
        return await planner_worker(task)

    # WATCH ROUTE
    if ttype == "watch_route":
        return await watch_worker(task)

    # ERROR FARE
    if ttype == "error_fare":
        return await errorfare_worker(task)

    return f"unknown task: {ttype}"


# -----------------------------
# WORKERS
# -----------------------------
async def route_worker(task):
    print("[ROUTE]", task["payload"])
    return "route done"


async def deal_worker(task):
    print("[DEALS]", task["payload"])
    return "deals done"


async def planner_worker(task):
    print("[PLANNER]", task["payload"])
    return "planner done"


async def watch_worker(task):
    print("[WATCH]", task["payload"])
    return "watch done"


async def errorfare_worker(task):
    print("[ERROR FARE]", task["payload"])
    return "errorfare done"


# -----------------------------
# POOL LOOP
# -----------------------------
async def run_pool():

    print(">>> WORKER POOL v1 STARTED")

    while True:

        tasks = claim(worker_id=WORKER_ID, limit=5)

        if not tasks:
            await asyncio.sleep(1)
            continue

        for task in tasks:
            try:
                result = await process_task(task)
                print("[DONE]", result)
                ack(task["id"])

            except Exception as e:
                print("[FAIL]", str(e))
                fail(task["id"], retry_delay_sec=30)


if __name__ == "__main__":
    asyncio.run(run_pool())
