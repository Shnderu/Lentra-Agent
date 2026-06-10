from core.queue.queue import claim, mark_done, mark_sent, mark_failed
from core.worker.handlers.route_search import handle as route_search_handler


async def process_once(bot, worker_id="w1"):
    tasks = claim(worker_id)

    for task in tasks:

        try:
            if task["type"] == "route_search":

                result = await route_search_handler(task)

                # 1. сохраняем результат
                mark_done(task["id"], result)

                # 2. отправка в Telegram (PRODUCTION FLOW)
                user_id = task["payload"]["user_id"]
                await bot.send_message(user_id, result)

                # 3. фиксируем отправку
                mark_sent(task["id"])

        except Exception as e:
            mark_failed(task["id"], str(e))
