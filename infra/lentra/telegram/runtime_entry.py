import asyncio
from lentra.telegram.runtime import TelegramRuntime


async def main():
    bot = TelegramRuntime()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
