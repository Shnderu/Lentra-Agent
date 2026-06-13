# ============================================================
# LENTRA TELEGRAM BOT - STRICT ENV MODE
# ============================================================

import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

ENV_PATH = "/opt/lentra/infra/.env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise Exception(f"Invalid BOT_TOKEN loaded: {BOT_TOKEN}")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

API_URL = "http://localhost:8000/search"


@dp.message()
async def handle_message(message: types.Message):
    payload = {
        "query": message.text,
        "budget": 500
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()

        best = data.get("best_choice", {})

        text = format_response(best, data.get("alternatives", []))

        await message.answer(text)

    except Exception as e:
        await message.answer(f"error: {str(e)}")


def format_response(best, alternatives):
    text = "🏠 BEST OPTION:\n"
    text += f"{best.get('title')} - ${best.get('price')}\n\n"

    if alternatives:
        text += "OTHER OPTIONS:\n"
        for a in alternatives:
            text += f"- {a.get('title')} - ${a.get('price')}\n"

    return text


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
