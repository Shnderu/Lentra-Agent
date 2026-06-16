import os
import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from lentra.bot.core.container import Container
from lentra.bot.handlers.router_builder import build_main_router


logging.basicConfig(level=logging.INFO)


async def main():
    print("[BOOT] ENTER MAIN", flush=True)

    container = Container()

    print("[BOOT] CONTAINER CREATED", flush=True)

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    print("[BOOT] TOKEN OK", flush=True)

    bot = Bot(token=token)
    dp = Dispatcher()

    print("[BOOT] BOT + DP CREATED", flush=True)

    router = build_main_router(container)

    print("[BOOT] ROUTER BUILT", flush=True)

    dp.include_router(router)

    print("[BOOT] ROUTER INCLUDED", flush=True)

    print("[BOOT] START POLLING", flush=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
