import os
import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

API_URL = os.getenv("LENTRA_API_URL", "http://127.0.0.1:8000/v1/search")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def search(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_URL,
            json={"query": query, "budget_max": 10},
            timeout=15
        ) as resp:
            return await resp.json()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Lentra Search Engine активирован.\n\n"
        "Отправь запрос, например:\n"
        "cheap apartment in Da Nang with pool"
    )


@dp.message()
async def handle_query(message: types.Message):
    query = message.text

    try:
        data = await search(query)
        results = data.get("results", [])

        if not results:
            await message.answer("Ничего не найдено.")
            return

        text = "Результаты:\n\n"

        for r in results[:5]:
            text += (
                f"ID: {r['id']}\n"
                f"{r['title']}\n"
                f"Цена: {r.get('price_vnd_mln', 'N/A')} млн VND\n"
                f"Score: {r.get('score', 0):.2f}\n"
                "-------------------\n"
            )

        await message.answer(text)

    except Exception as e:
        logging.exception(e)
        await message.answer("Ошибка обработки запроса.")


async def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
