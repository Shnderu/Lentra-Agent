import asyncio
import asyncpg
import os
import traceback

from app.core.gateway.execution_entry_v1 import execute as gateway_execute
from lentra.db.queue import PostgresQueue

DB_DSN = os.getenv("DB_DSN")


async def process_task(task):
    """
    Все задачи теперь идут через единый gateway
    """
    result = gateway_execute(task)
    print(f"[WORKER] {task['task_type']} -> {result.get('ok', True)}")


async def init_gateway():
    """
    FIX: IntentRouter теперь требует registry
    """
    from lentra.bot.core.container import Container
    from lentra.bot.core.feature_registry import FeatureRegistry
    from lentra.bot.core.intent_router import IntentRouter
    from lentra.bot.core.intent_resolver import IntentResolver

    registry = FeatureRegistry()

    intent_router = IntentRouter(registry=registry)
    intent_resolver = IntentResolver(feature_registry=registry)

    return intent_router, intent_resolver


async def worker_loop():
    pool = await asyncpg.create_pool(dsn=DB_DSN, min_size=1, max_size=10)
    queue = PostgresQueue(pool)

    print("[WORKER] STARTED")

    # FIX: инициализация gateway зависимостей
    try:
        await init_gateway()
    except Exception as e:
        print("[WORKER INIT ERROR]", str(e))
        traceback.print_exc()

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
                await queue.mark_failed(task["id"], str(e))

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
