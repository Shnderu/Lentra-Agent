import os
import asyncio

from aiogram import Bot, Dispatcher

from lentra.bot.core.container import Container
from lentra.bot.handlers.router_builder import build_main_router


async def main():

    print("[BOOT] ENTER MAIN")

    container = Container()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=token)
    dp = Dispatcher()

    print("[BOOT] BOT + DP CREATED")

    router = build_main_router(container)

    print("[BOOT] ROUTER BUILT")

    dp.include_router(router)

    print("[BOOT] ROUTER INCLUDED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
