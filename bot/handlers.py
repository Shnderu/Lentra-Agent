from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import time

from api import create_task, get_task

router = Router()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Rent Search")]
    ],
    resize_keyboard=True
)


@router.message()
async def handle(message: types.Message):

    if message.text == "🏠 Rent Search":
        await message.answer("Send city name:")
        return

    city = message.text

    task_id = create_task({
        "type": "rent.search",
        "payload": {
            "city": city,
            "budget": 1000
        }
    })

    await message.answer(f"Searching rentals in {city}...")

    # polling
    for _ in range(10):
        time.sleep(1)
        task = get_task(task_id)

        if task.get("status") == "done":
            results = task["result"]["results"][:5]

            text = "🏠 Results:\n\n"
            for r in results:
                text += f"{r['title']} - {r['price']}\n"

            await message.answer(text)
            return

    await message.answer("Timeout. Try again.")
