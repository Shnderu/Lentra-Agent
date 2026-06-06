from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.engine.postgres_queue import push_task

router = Router()


@router.message(Command("add_flight"))
async def add_flight(message: Message):
    parts = message.text.split()

    if len(parts) < 3:
        await message.answer("Использование: /add_flight MOW DXB")
        return

    origin = parts[1]
    destination = parts[2]

    try:
        task_id = push_task(
            "flight_search",
            {
                "user_id": message.from_user.id,
                "origin": origin,
                "destination": destination,
            },
            priority=5,
        )

        await message.answer(
            f"✈️ Задача создана\nID: {task_id}\n{origin} → {destination}"
        )

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
