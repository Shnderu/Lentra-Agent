import logging
from aiogram import Router, types
from aiogram.filters import Command

from bot.services.routes import add_route

router = Router()


@router.message(Command("add_flight"))
async def add_flight(message: types.Message):
    try:
        user_id = message.from_user.id

        # пример: текст после команды
        route = message.text.replace("/add_flight", "").strip()

        if not route:
            await message.answer("⚠️ Укажи маршрут: /add_flight MOW → DXB")
            return

        result = add_route(user_id, route)

        if not result:
            await message.answer("❌ Ошибка сохранения маршрута. Попробуйте позже.")
            return

        await message.answer(f"✅ Маршрут сохранён: {route}")

    except Exception as e:
        logging.error(f"[HANDLER:add_flight] unexpected error: {e}")
        await message.answer("❌ Внутренняя ошибка обработки запроса")
