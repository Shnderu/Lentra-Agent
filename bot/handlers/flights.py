from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.routes import add_route

router = Router()


@router.message(Command("add_flight"))
async def add_flight(message: Message):
    try:
        parts = message.text.split()

        if len(parts) < 3:
            await message.answer("Использование: /add_flight MOW DXB")
            return

        origin = parts[1]
        destination = parts[2]

        task_id = add_route(
            user_id=message.from_user.id,
            route=f"{origin}-{destination}"
        )

        await message.answer(
            f"✈️ Задача создана\nID: {task_id}\n{origin} → {destination}"
        )

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
