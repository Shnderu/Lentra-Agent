import asyncio

from lentra.bot.core.container import build_container
from lentra.bot.handlers.router_builder import build_main_router
from lentra.bot.adapters.telegram_update_adapter import TelegramUpdateAdapter
from lentra.bot.runtime.trace import Trace


def main():
    print("[BOOT] ENTER MAIN")

    container = build_container()
    router = build_main_router(container)

    adapter = TelegramUpdateAdapter()

    async def process_update(tg_update: dict):

        trace = Trace()
        container.trace = trace
        adapter.trace = trace

        update = adapter.normalize(tg_update)
        result = await router.handle(update)

        print("===== TRACE DUMP =====")
        print(trace.dump())
        print("======================")
        print("[RESULT]", result)

        return result


    async def mock_stream():
        while True:
            tg_update = {
                "update_id": 1,
                "message": {
                    "text": "rent apartment",
                    "from": {"id": 123}
                }
            }

            await process_update(tg_update)
            await asyncio.sleep(5)


    asyncio.run(mock_stream())


if __name__ == "__main__":
    main()
