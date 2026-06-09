from core.queue.queue import claim
from core.worker.handlers.route_search import handle as route_search_handler


async def process_once(worker_id="w1"):
    tasks = claim(worker_id)

    for task in tasks:

        if task["type"] == "route_search":
            await route_search_handler(task)
