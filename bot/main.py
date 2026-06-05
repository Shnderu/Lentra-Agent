import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramUnauthorizedError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

async def main():
    token = os.getenv("BOT_TOKEN")

    # 🔴 ЖЁСТКАЯ ПРОВЕРКА (ВАЖНО)
    if not token:
        logging.error("BOT_TOKEN is NOT set. Check .env file.")
        raise RuntimeError("BOT_TOKEN is missing")

    try:
        bot = Bot(token=token)
        dp = Dispatcher()

        logging.info("Bot starting...")

        # старт polling
        await dp.start_polling(bot)

    except TelegramUnauthorizedError:
        logging.error("Telegram Unauthorized: invalid BOT_TOKEN")
        raise

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
